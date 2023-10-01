from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'Products'

    ProductID = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String(255), nullable=False)
    CategoryID = Column(Integer, ForeignKey('Categories.CategoryID'), nullable=False)
    # Define one-to-many relationship with Sales
    sales = relationship('Sale', back_populates='product')
    inventory = relationship('Inventory', back_populates='product')
    inventory_log = relationship('InventoryLog', back_populates='product')
    low_stock_alerts = relationship('LowStockAlert', back_populates='product')

class Category(Base):
    __tablename__ = 'Categories'

    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String(255), nullable=False)
    # Define one-to-many relationship with Sales
    sales = relationship('Sale', back_populates='category')

class Sale(Base):
    __tablename__ = 'Sales'

    SaleID = Column(Integer, primary_key=True)
    SaleDate = Column(Date, nullable=False)
    ProductID = Column(Integer, ForeignKey('Products.ProductID'), nullable=False)
    CategoryID = Column(Integer, ForeignKey('Categories.CategoryID'), nullable=False)
    Quantity = Column(Integer, nullable=False)
    Price = Column(Float(precision=2), nullable=False)

    # Define many-to-one relationships with Products and Categories
    product = relationship('Product', back_populates='sales')
    category = relationship('Category', back_populates='sales')

class Inventory(Base):
    __tablename__ = 'Inventory'

    InventoryID = Column(Integer, primary_key=True)
    ProductID = Column(Integer, ForeignKey('Products.ProductID'), nullable=False)
    Quantity = Column(Integer, nullable=False)

    # Define many-to-one relationship with Products
    product = relationship('Product', back_populates='inventory')

class InventoryLog(Base):
    __tablename__ = 'Inventory_Log'

    LogID = Column(Integer, primary_key=True)
    ProductID = Column(Integer, ForeignKey('Products.ProductID'), nullable=False)
    QuantityChange = Column(Integer, nullable=False)
    ChangeDate = Column(DateTime, nullable=False)

    # Define many-to-one relationship with Products
    product = relationship('Product', back_populates='inventory_log')

class LowStockAlert(Base):
    __tablename__ = 'Low_Stock_Alerts'

    AlertID = Column(Integer, primary_key=True)
    ProductID = Column(Integer, ForeignKey('Products.ProductID'), nullable=False)
    AlertThreshold = Column(Integer, nullable=False)

    # Define many-to-one relationship with Products
    product = relationship('Product', back_populates='low_stock_alerts')
