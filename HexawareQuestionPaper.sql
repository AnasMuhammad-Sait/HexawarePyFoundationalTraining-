CREATE DATABASE TEST;
USE TEST;

-- Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(100),
    City VARCHAR(100)
);

-- Orders Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    Amount DECIMAL(10,2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Products Table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Price DECIMAL(10,2)
);

-- OrderDetails Table
CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

INSERT INTO Customers (CustomerID, Name, City) VALUES
(1, 'John', 'Delhi'),
(2, 'Priya', 'Mumbai'),
(3, 'Amit', 'Delhi'),
(4, 'Sara', 'Chennai'),
(5, 'Ravi', 'Kolkata'),
(6, 'Sneha', 'Bangalore');

INSERT INTO Products (ProductID, ProductName, Price) VALUES
(101, 'Laptop', 55000),
(102, 'Phone', 30000),
(103, 'Headphones', 1500),
(104, 'Mouse', 500),
(105, 'Keyboard', 1200),
(106, 'Monitor', 7000);

INSERT INTO Orders (OrderID, CustomerID, OrderDate, Amount) VALUES
(1001, 1, '2024-12-01', 55000),
(1002, 2, '2024-12-01', 1500),
(1003, 3, '2024-12-02', 30000),
(1004, 4, '2024-11-20', 500),
(1005, 1, '2024-12-03', 1200),
(1006, 5, CURDATE(), 7000),
(1007, 6, CURDATE() - INTERVAL 10 DAY, 5000),
(1008, 1, CURDATE() - INTERVAL 5 DAY, 35000),
(1009, 3, CURDATE() - INTERVAL 30 DAY, 500),
(1010, 3, CURDATE() - INTERVAL 3 DAY, 1500);

INSERT INTO OrderDetails (OrderDetailID, OrderID, ProductID, Quantity) VALUES
(201, 1001, 101, 1),   
(202, 1002, 103, 1),  
(203, 1003, 102, 1),
(204, 1004, 104, 1), 
(205, 1005, 105, 1),
(206, 1006, 106, 1),   
(207, 1007, 101, 1),     
(208, 1008, 102, 1),    
(209, 1008, 103, 2),    
(210, 1009, 104, 1),  
(211, 1010, 103, 3); 

-- Question 1 
SELECT c.CustomerID, c.Name
FROM Customers c
WHERE NOT EXISTS (
    SELECT DISTINCT MONTH(CURDATE()) - m.month_val
    FROM (
        SELECT 1 AS month_val UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
        UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12
    ) m
    WHERE NOT EXISTS (
        SELECT 1 FROM Orders o
        WHERE o.CustomerID = c.CustomerID
        AND YEAR(o.OrderDate) = YEAR(CURDATE())
        AND MONTH(o.OrderDate) = m.month_val
    )
);

-- Question 2 
SELECT p.ProductName
FROM Products p
JOIN OrderDetails od ON p.ProductID = od.ProductID
GROUP BY p.ProductID
HAVING SUM(od.Quantity) > (
    SELECT AVG(quantity_sum) FROM (
        SELECT SUM(Quantity) AS quantity_sum
        FROM OrderDetails
        GROUP BY ProductID
    ) avg_table
);

-- Question 3 
SELECT c.CustomerID, c.Name
FROM Customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM Orders o
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    JOIN Products p ON od.ProductID = p.ProductID
    WHERE c.CustomerID = o.CustomerID
    AND p.Price > 1000
);

-- Question 4 
SELECT ProductID, ProductName, total_revenue
FROM (
    SELECT p.ProductID, p.ProductName, SUM(od.Quantity * p.Price) AS total_revenue
    FROM Products p
    JOIN OrderDetails od ON p.ProductID = od.ProductID
    GROUP BY p.ProductID
    ORDER BY total_revenue DESC
    LIMIT 3
) AS TopProducts;

-- Question 5 
SELECT o.OrderID
FROM Orders o
WHERE 1 = (
    SELECT COUNT(*)
    FROM OrderDetails od
    WHERE od.OrderID = o.OrderID
);
 
-- Question 6
SELECT DISTINCT c.Name
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderDate IN (
    SELECT OrderDate FROM Orders o2
    JOIN Customers c2 ON o2.CustomerID = c2.CustomerID
    WHERE c2.Name = 'John'
);

-- Question 7
SELECT c.Name
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderDate = (SELECT MAX(OrderDate) FROM Orders);

-- Question 8
SELECT ProductName
FROM Products
WHERE Price = (
    SELECT DISTINCT Price
    FROM Products
    ORDER BY Price ASC
    LIMIT 1 OFFSET 1
);

-- Question 9
SELECT c.Name
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID
HAVING SUM(o.Amount) > 2 * (
    SELECT AVG(total_spending)
    FROM (
        SELECT CustomerID, SUM(Amount) AS total_spending
        FROM Orders
        GROUP BY CustomerID
    ) avg_spend
);

-- Question 10
SELECT c.CustomerID, c.Name
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID
HAVING SUM(o.Amount) > ANY (
    SELECT SUM(o2.Amount)
    FROM Orders o2
    JOIN Customers c2 ON o2.CustomerID = c2.CustomerID
    WHERE c2.City = 'Delhi'
    GROUP BY c2.CustomerID
);

-- Question 11
SELECT c.Name
FROM Customers c
WHERE (
    SELECT COUNT(*) FROM Orders o WHERE o.CustomerID = c.CustomerID
) > (
    SELECT AVG(order_count) FROM (
        SELECT CustomerID, COUNT(*) AS order_count
        FROM Orders
        GROUP BY CustomerID
    ) counts
);

-- Question 12
SELECT p.ProductName
FROM Products p
JOIN OrderDetails od ON p.ProductID = od.ProductID
GROUP BY p.ProductID
HAVING SUM(od.Quantity) > (
    SELECT AVG(total_qty) FROM (
        SELECT SUM(Quantity) AS total_qty
        FROM OrderDetails
        GROUP BY ProductID
    ) q
);

-- Question 13
SELECT DISTINCT c.CustomerID, c.Name
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN OrderDetails od ON o.OrderID = od.OrderID
WHERE od.ProductID IN (
    SELECT ProductID FROM OrderDetails
    GROUP BY ProductID
    HAVING COUNT(DISTINCT OrderID) = 1
);

-- Question 14
SELECT o.*
FROM Orders o
WHERE o.Amount = (
    SELECT MAX(o2.Amount) FROM Orders o2 WHERE o2.CustomerID = o.CustomerID
);

-- Question 15	
SELECT DISTINCT c.CustomerID, c.Name
FROM Customers c
WHERE c.CustomerID NOT IN (
    SELECT o.CustomerID
    FROM Orders o
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    WHERE od.Quantity > 5
);

-- Question 16
SELECT c.CustomerID, c.Name, SUM(o.Amount) AS TotalSpent
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID
ORDER BY TotalSpent DESC
LIMIT 5;

-- Question 17
SELECT c.CustomerID, c.Name
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN OrderDetails od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID
HAVING COUNT(DISTINCT od.ProductID) = 1;

-- Question 18 
SELECT * FROM Orders
WHERE Amount NOT IN (
    SELECT Amount FROM Orders
    ORDER BY Amount DESC
    LIMIT 10
);

-- Question 19
SELECT DISTINCT c.Name
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderDate BETWEEN CURDATE() - INTERVAL 7 DAY AND CURDATE()
AND c.CustomerID NOT IN (
    SELECT CustomerID FROM Orders
    WHERE OrderDate BETWEEN CURDATE() - INTERVAL 37 DAY AND CURDATE() - INTERVAL 8 DAY
);

-- Question 20 
SELECT ProductID, ProductName
FROM Products
WHERE ProductID IN (
    SELECT ProductID
    FROM OrderDetails
    GROUP BY ProductID
    HAVING COUNT(DISTINCT OrderID) = (
        SELECT MAX(order_count) FROM (
            SELECT COUNT(DISTINCT OrderID) AS order_count
            FROM OrderDetails
            GROUP BY ProductID
        ) x
    )
);

