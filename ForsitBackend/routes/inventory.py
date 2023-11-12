import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ForsitBackend.plogger import PLogger
from ..database import get_db
from ..models import Inventory, InventoryLog, Product, LowStockAlert, Category
from .. import schemas
from datetime import datetime

logger = PLogger(name="my_fastapi_logger", level=logging.INFO).get_logger()


router = APIRouter()

@router.get("/")
def get_inventory_status(
    product_id: int = None,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    logger.info(f"Received a request on the inventory root endpoint with params product_id={product_id}, catgory_id={category_id}")
    try:
        # Retrieve inventory status based on product_id and category_id
        if product_id:
            inventory_entry = db.query(Inventory).filter(Inventory.ProductID == product_id).first()
            if not inventory_entry:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found in the inventory")
            return {"product_id": product_id, "quantity": inventory_entry.Quantity}

        if category_id:
            products_in_category = db.query(Product).join(Category).filter(Category.CategoryID == category_id).all()
            inventory_status = []
            for product in products_in_category:
                inventory_entry = db.query(Inventory).filter(Inventory.ProductID == product.ProductID).first()
                if inventory_entry:
                    inventory_status.append({"product_id": product.ProductID, "product_name": product.ProductName, "quantity": inventory_entry.Quantity})
                else:
                    inventory_status.append({"product_id": product.ProductID, "product_name": product.ProductName, "quantity": 0})
            return inventory_status

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either product_id or category_id should be provided")

    except Exception as e:
        # Log the exception for debugging purposes
        logger.error(f"Exception Occurred :: {e}")

        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.post("/add-category/")
def add_new_category_to_inventory(
    request: schemas.CategorySchema,
    db: Session = Depends(get_db)
):
    logger.info(f"Received a request on the inventory add-category ")
    try:
        existing_category = db.query(Category).filter(Category.CategoryName == request.category_name).first()
        if existing_category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists in the inventory")
        new_category = Category(CategoryName= request.category_name)
        db.add(new_category)
        db.commit()
        return {"message":"Category added to inventory successfully"}
    except Exception as e:
        # If an exception occurs, rollback the transaction
        db.rollback()
        # Add logs for debugging purpose
        logger.error("Internal Server Error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')

@router.post("/add-product/")
def add_new_product_to_inventory(
    request: schemas.ProdcutSchema,
    db: Session = Depends(get_db)
):
    logger.info(f"Received a request on the inventory add-product")
    try:
        # Check if the product already exists in the database
        existing_product = db.query(Product).filter(Product.ProductName == request.product_name).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="Product already exists in the inventory")
        
        related_category = db.query(Category).filter(Category.CategoryName == request.categoty_name).first()
        if not related_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category is not Present in inventory')

        # Create a new product
        new_product = Product(ProductName=request.product_name, CategoryID=related_category.CategoryID)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        # Add the product to the inventory with the initial quantity
        new_inventory_entry = Inventory(ProductID=new_product.ProductID, Quantity=request.initial_quantity)
        db.add(new_inventory_entry)
        db.commit()
        db.refresh(new_inventory_entry)
        # Log the inventory change
        inventory_log_entry = InventoryLog(ProductID=new_product.ProductID, QuantityChange=request.initial_quantity, ChangeDate= datetime.now())
        db.add(inventory_log_entry)
        db.commit()
        return {"message": "Product added to inventory successfully"}

    except Exception as e:
        # If an exception occurs, rollback the transaction
        db.rollback()
        logger.error(f'Exception :: {e}')
        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/update/")
def update_inventory(
    request: schemas.InventorySchema,
    db: Session = Depends(get_db)
):
    logger.info("Received a request on the inventory Update")
    try:
        # Check if the product exists
        product = db.query(Product).filter(Product.ProductID == request.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Update inventory levels for the specified product
        inventory_entry = db.query(Inventory).filter(Inventory.ProductID == request.product_id).first()
        if not inventory_entry:
            raise HTTPException(status_code=500, detail="Internal Server Error")

        # Update the inventory quantity
        inventory_entry.Quantity += request.quantity_change
        db.commit()

        # Log the inventory change
        inventory_log_entry = InventoryLog(ProductID=request.product_id, QuantityChange=request.quantity_change, ChangeDate= datetime.now())
        db.add(inventory_log_entry)
        db.commit()

        

        # Return the updated inventory status
        return {
            "message": "Inventory updated successfully",
            "product_id": request.product_id,
            "new_quantity": inventory_entry.Quantity
        }
    except Exception as e:
        # If an exception occurs, rollback the transaction
        db.rollback()
        logger.error(f'Exception :: {e}')
        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/low-stock-alerts/")
def get_low_stock_alerts(
    db: Session = Depends(get_db)
):
    # Retrieve products with low stock levels from LowStockAlert table
    logger.info("Received a request on the inventory low-stock-alert")
    low_stock_products = db.query(LowStockAlert).all()

    if not low_stock_products:
        raise HTTPException(500, 'Stock is unavailable')

    # Fetch product details for low stock products
    low_stock_product_details = []
    for alert in low_stock_products:
        product = db.query(Product).filter(Product.ProductID == alert.ProductID).first()
        if product:
            low_stock_product_details.append({
                "product_id": product.ProductID,
                "product_name": product.ProductName,
                "current_quantity": alert.AlertThreshold
            })

    return low_stock_product_details