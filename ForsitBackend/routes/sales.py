from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Sale, Category, Product
from datetime import datetime
from ..service import calculate_daily_revenue,calculate_weekly_revenue, calculate_monthly_revenue, calculate_annual_revenue,calculate_revenue

router = APIRouter()

@router.get("/")
def get_sales_data(
    start_date: str = None,
    end_date: str = None,
    product_id: int = None,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    try:
        # Parse start_date and end_date parameters to datetime objects if provided
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

        # Base query to filter sales data
        query = db.query(Sale)

        # Apply filters based on parameters
        if parsed_start_date:
            query = query.filter(Sale.SaleDate >= parsed_start_date)
        if parsed_end_date:
            query = query.filter(Sale.SaleDate <= parsed_end_date)
        if product_id:
            query = query.filter(Sale.ProductID == product_id)
        if category_id:
            query = query.join(Product).join(Category).filter(Category.CategoryID == category_id)

        # Retrieve filtered sales data
        sales_data = query.all()

        # Prepare the response data
        response_data = []
        for sale in sales_data:
            response_data.append({
                "sale_id": sale.SaleID,
                "sale_date": sale.SaleDate,
                "product_id": sale.ProductID,
                "quantity": sale.Quantity,
                "price": sale.Price
            })

        return response_data

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Please provide dates in YYYY-MM-DD format.")
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error: {e}")

        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.get("/revenue/")
def get_revenue_data(
    start_date: str = None,
    end_date: str = None,
    period: str = None,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    try:
        # Parse start_date and end_date parameters to datetime objects if provided
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

        # Base query to filter sales data
        query = db.query(Sale)

        # Apply filters based on parameters
        if parsed_start_date:
            query = query.filter(Sale.SaleDate >= parsed_start_date)
        if parsed_end_date:
            query = query.filter(Sale.SaleDate <= parsed_end_date)
        if category_id:
            query = query.join(Product).join(Category).filter(Category.CategoryID == category_id)

        # Retrieve filtered sales data
        sales_data = query.all()

        # Calculate revenue based on the specified period
        if period == "daily":
            revenue_data = calculate_daily_revenue(sales_data)
        elif period == "weekly":
            revenue_data = calculate_weekly_revenue(sales_data)
        elif period == "monthly":
            revenue_data = calculate_monthly_revenue(sales_data)
        elif period == "annual":
            revenue_data = calculate_annual_revenue(sales_data)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid period. Supported periods: daily, weekly, monthly, annual.")

        return revenue_data

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Please provide dates in YYYY-MM-DD format.")
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error: {e}")

        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )




@router.get("/compare/")
def compare_revenue(
    start_date: str = None,
    end_date: str = None,
    category_id: int = None,
    frequency: str = 'daily',
    db: Session = Depends(get_db)
):
    try:
        # Parse start_date and end_date parameters to datetime objects if provided
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

        # Base query to filter sales data
        query = db.query(Sale)

        # Apply filters based on parameters
        if parsed_start_date:
            query = query.filter(Sale.SaleDate >= parsed_start_date)
        if parsed_end_date:
            query = query.filter(Sale.SaleDate <= parsed_end_date)
        if category_id:
            query = query.join(Product).join(Category).filter(Category.CategoryID == category_id)

        # Retrieve filtered sales data
        sales_data = query.all()

        # Calculate revenue based on the specified frequency
        revenue_data = calculate_revenue(sales_data, frequency)

        return revenue_data

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Please provide dates in YYYY-MM-DD format.")
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error: {e}")

        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )