-- Products Table
INSERT INTO Products (ProductID, ProductName,CategoryID) VALUES (1, 'Laptop',1);
INSERT INTO Products (ProductID, ProductName,CategoryID) VALUES (2, 'Smartphone',2);
INSERT INTO Products (ProductID, ProductName,CategoryID) VALUES (3, 'Tablet',2);

-- Categories Table
INSERT INTO Categories (CategoryID, CategoryName) VALUES (1, 'Electronics');
INSERT INTO Categories (CategoryID, CategoryName) VALUES (2, 'Mobile Devices');

-- Sales Table
INSERT INTO Sales (SaleID, SaleDate, ProductID, CategoryID, Quantity, Price) VALUES (1, '2023-09-01', 1, 1, 2, 800.00);
INSERT INTO Sales (SaleID, SaleDate, ProductID, CategoryID, Quantity, Price) VALUES (2, '2023-09-02', 2, 2, 3, 600.00);
INSERT INTO Sales (SaleID, SaleDate, ProductID, CategoryID, Quantity, Price) VALUES (3, '2023-09-03', 3, 1, 1, 300.00);

-- Inventory Table
INSERT INTO Inventory (InventoryID, ProductID, Quantity) VALUES (1, 1, 10);
INSERT INTO Inventory (InventoryID, ProductID, Quantity) VALUES (2, 2, 15);
INSERT INTO Inventory (InventoryID, ProductID, Quantity) VALUES (3, 3, 8);

-- Inventory_Log Table
INSERT INTO Inventory_Log (LogID, ProductID, QuantityChange, ChangeDate) VALUES (1, 1, -2, '2023-09-01 10:30:00');
INSERT INTO Inventory_Log (LogID, ProductID, QuantityChange, ChangeDate) VALUES (2, 2, -3, '2023-09-02 14:45:00');
INSERT INTO Inventory_Log (LogID, ProductID, QuantityChange, ChangeDate) VALUES (3, 3, -1, '2023-09-03 09:15:00');

-- Low_Stock_Alerts Table
INSERT INTO Low_Stock_Alerts (AlertID, ProductID, AlertThreshold) VALUES (1, 1, 5);
INSERT INTO Low_Stock_Alerts (AlertID, ProductID, AlertThreshold) VALUES (2, 2, 7);
INSERT INTO Low_Stock_Alerts (AlertID, ProductID, AlertThreshold) VALUES (3, 3, 3);
