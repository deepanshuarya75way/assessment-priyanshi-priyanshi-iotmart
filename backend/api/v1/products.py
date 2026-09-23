from fastapi import APIRouter, HTTPException, Body, UploadFile, File
import os
import shutil
import uuid
from typing import List
from schemas.product import Product, ProductCreate
from repositories.product_repo import product_repo
from bson import ObjectId
from fastapi import Depends
from api.deps import get_current_active_admin
from core.redis_cache import get_cache , set_cache
from repositories.order_repo import order_repo
from core.database import db
from api.deps import get_current_active_admin
from fastapi import Depends
router = APIRouter()

from core.redis_cache import get_cache, set_cache, delete_cache

@router.get("/")
async def get_products(page: int = 1, limit: int = 100):
    print("DEBUG: Inside get_products")
    cache_key = f"products:page:{page}:limit:{limit}"
    print("DEBUG: Checking cache")
    cached_data = await get_cache(cache_key)
    print("DEBUG: Cache check done")
    if cached_data:
        return cached_data

    skip = (page - 1) * limit
    print("DEBUG: Querying DB")
    products = await product_repo.get_all_products(skip, limit)
    print("DEBUG: Query done")
    for product in products:
        product["_id"] = str(product["_id"])
    
    total = await product_repo.count_products()
    result = {
        "products": products,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit
    }
    
    await set_cache(cache_key, result, expire=300) # cache for 5 mins
    return result

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate = Body(...), current_user: dict = Depends(get_current_active_admin)):
    new_product = await product_repo.insert_product(product.model_dump())
    created_product = await product_repo.get_product_by_id(str(new_product.inserted_id))
    created_product["_id"] = str(created_product["_id"])
    
    await delete_cache("products:page:*")
    return created_product

@router.get("/{id}", response_model=Product)
async def get_product(id: str):
    product = await product_repo.get_product_by_id(id)
    if product:
        product["_id"] = str(product["_id"])
        return product
    raise HTTPException(status_code=404, detail="Product not found")
@router.get("/{id}/recommandations")
async def get_recommandations(id:str, limit: int = 4):
    cache_key = f"reco:product:{id}"
    cached = await get_cache (cache_key)
    if cached:
        return cached 

    product = await product_repo.get_product_by_id(id)
    if not product :
        return cached

    results = await product_repo.get_similar_products(product["category"], id , limit)
    if not results   :
        results = await product_repo.get_popular_products(limit)


    await set_cache(cache_key, results, expire=3600)
    return results

@router.post("/recommandations/cart")
async def get_cart_recommandations(product_ids: list[str], limit : int = 4):
    if not product_ids:
        return[]
    
    orders = await order_repo.get_orders_containing(product_ids)
    freq = {}
    for order in orders:
        for item in order ["items"]:
            pid = str(item["product_id"])
            if pid not in product_ids:
                freq[pid] = Freq.get(pid,0)+ 1 

        top_ids = sorted(freq, key= freq.get , reverse = true )[:limit]
        if not top_ids:
            return await product_repo.get_popular_products(limit)

        products = [await products_repo.get_product_by_id(pid) for pid in top_ids]
        return [p for p in products if p]    

@router.get("/settings/recommandations")
async def get_recommandations_settings():
    setting = await db.settings.find_one({"key": "recommandations_enabled"})
    return {"enabled": setting ["value"] if setting else true}

@router.put("/settings/recommandations")
async def toggle_recommandations(enabled:bool, admin=Depends(get_current_active_admin)):
    await db.settings.update_one(
        {"key": "recommandations_enabled"},
        {"$set" : {"value": enabled}},
        upsert = true
    )
    return{ "enabled" : enabled}
@router.put("/{id}", response_model=Product)
async def update_product(id: str, product: ProductCreate = Body(...), current_user: dict = Depends(get_current_active_admin)):
    updated = await product_repo.update_product(id, product.model_dump())
    if updated.modified_count:
        product_data = await product_repo.get_product_by_id(id)
        product_data["_id"] = str(product_data["_id"])
        
        await delete_cache("products:page:*")
        return product_data
    raise HTTPException(status_code=404, detail="Product not found or no changes made")

@router.delete("/{id}")
async def delete_product(id: str, current_user: dict = Depends(get_current_active_admin)):
    result = await product_repo.delete_product(id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await delete_cache("products:page:1:limit:100")
    return {"success": True, "message": "Product deleted successfully"}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
        
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Assuming frontend URL maps /uploads to backend's UPLOAD_DIR
    # In production, we'd use S3/Cloudinary URL
    # For now we return local path that FastAPI will serve statically
    image_url = f"/uploads/{filename}"
    return {"success": True, "image_url": image_url}

@router.post("/{id}/reviews")
async def add_review(id: str, review: dict = Body(...)):
    product = await product_repo.get_product_by_id(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    user_id = review.get("user_id")
    verified_buyer = False
    
    if user_id:
        # Check if user has placed an order containing this product
        from core.database import db
        order = await db.orders.find_one({
            "user_id": user_id, 
            "items.product_id": id
        })
        if order:
            verified_buyer = True
            
    review["verified_buyer"] = verified_buyer
    
    reviews = product.get("reviews", [])
    reviews.append(review)
    
    # Simple average rating calculation
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
    
    await product_repo.update_product(id, {
        "reviews": reviews,
        "reviews_count": len(reviews),
        "rating": round(avg_rating, 1)
    })
    return {"message": "Review added", "rating": avg_rating}
