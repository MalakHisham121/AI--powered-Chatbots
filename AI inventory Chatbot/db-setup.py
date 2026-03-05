
db_schema = [
    '''CREATE TABLE IF NOT EXISTS Customers (
        CustomerId INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerCode VARCHAR(50) UNIQUE NOT NULL,
        CustomerName NVARCHAR(200) NOT NULL,
        Email NVARCHAR(200) NULL,
        Phone NVARCHAR(50) NULL,
        BillingAddress1 NVARCHAR(200) NULL,
        BillingCity NVARCHAR(100) NULL,
        BillingCountry NVARCHAR(100) NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );''',
    '''CREATE TABLE IF NOT EXISTS Vendors (
        VendorId INTEGER PRIMARY KEY AUTOINCREMENT,
        VendorCode VARCHAR(50) UNIQUE NOT NULL,
        VendorName NVARCHAR(200) NOT NULL,
        Email NVARCHAR(200) NULL,
        Phone NVARCHAR(50) NULL,
        AddressLine1 NVARCHAR(200) NULL,
        City NVARCHAR(100) NULL,
        Country NVARCHAR(100) NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );''',
    '''CREATE TABLE IF NOT EXISTS Sites (
        SiteId INTEGER PRIMARY KEY AUTOINCREMENT,
        SiteCode VARCHAR(50) UNIQUE NOT NULL,
        SiteName NVARCHAR(200) NOT NULL,
        AddressLine1 NVARCHAR(200) NULL,
        City NVARCHAR(100) NULL,
        Country NVARCHAR(100) NULL,
        TimeZone NVARCHAR(100) NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );''',
    '''CREATE TABLE IF NOT EXISTS Locations (
        LocationId INTEGER PRIMARY KEY AUTOINCREMENT,
        SiteId INT NOT NULL,
        LocationCode VARCHAR(50) NOT NULL,
        LocationName NVARCHAR(200) NOT NULL,
        ParentLocationId INT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive BIT NOT NULL DEFAULT 1,
        CONSTRAINT UQ_Locations_SiteCode UNIQUE (SiteId, LocationCode),
        CONSTRAINT FK_Locations_Site FOREIGN KEY (SiteId) REFERENCES Sites(SiteId),
        CONSTRAINT FK_Locations_Parent FOREIGN KEY (ParentLocationId) REFERENCES Locations(LocationId)
    );''',
    '''CREATE TABLE IF NOT EXISTS Items (
        ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
        ItemCode NVARCHAR(100) UNIQUE NOT NULL,
        ItemName NVARCHAR(200) NOT NULL,
        Category NVARCHAR(100) NULL,
        UnitOfMeasure NVARCHAR(50) NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );''',
    '''CREATE TABLE IF NOT EXISTS Assets (
        AssetId INTEGER PRIMARY KEY AUTOINCREMENT,
        AssetTag VARCHAR(100) UNIQUE NOT NULL,
        AssetName NVARCHAR(200) NOT NULL,
        SiteId INT NOT NULL,
        LocationId INT NULL,
        SerialNumber NVARCHAR(200) NULL,
        Category NVARCHAR(100) NULL,
        Status VARCHAR(30) NOT NULL DEFAULT 'Active',
        Cost DECIMAL(18,2) NULL,
        PurchaseDate DATE NULL,
        VendorId INT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        CONSTRAINT FK_Assets_Site FOREIGN KEY (SiteId) REFERENCES Sites(SiteId),
        CONSTRAINT FK_Assets_Location FOREIGN KEY (LocationId) REFERENCES Locations(LocationId),
        CONSTRAINT FK_Assets_Vendor FOREIGN KEY (VendorId) REFERENCES Vendors(VendorId)
    );''',
    '''CREATE TABLE IF NOT EXISTS Bills (
        BillId INTEGER PRIMARY KEY AUTOINCREMENT,
        VendorId INT NOT NULL,
        BillNumber VARCHAR(100) NOT NULL,
        BillDate DATE NOT NULL,
        DueDate DATE NULL,
        TotalAmount DECIMAL(18,2) NOT NULL,
        Currency VARCHAR(10) NOT NULL DEFAULT 'USD',
        Status VARCHAR(30) NOT NULL DEFAULT 'Open',
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        CONSTRAINT UQ_Bills_Vendor_BillNumber UNIQUE (VendorId, BillNumber),
        CONSTRAINT FK_Bills_Vendor FOREIGN KEY (VendorId) REFERENCES Vendors(VendorId)
    );''',
    '''CREATE TABLE IF NOT EXISTS PurchaseOrders (
        POId INTEGER PRIMARY KEY AUTOINCREMENT,
        PONumber VARCHAR(100) NOT NULL,
        VendorId INT NOT NULL,
        PODate DATE NOT NULL,
        Status VARCHAR(30) NOT NULL DEFAULT 'Open',
        SiteId INT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        CONSTRAINT UQ_PurchaseOrders_Number UNIQUE (PONumber),
        CONSTRAINT FK_PurchaseOrders_Vendor FOREIGN KEY (VendorId) REFERENCES Vendors(VendorId),
        CONSTRAINT FK_PurchaseOrders_Site FOREIGN KEY (SiteId) REFERENCES Sites(SiteId)
    );''',
    '''CREATE TABLE IF NOT EXISTS PurchaseOrderLines (
        POLineId INTEGER PRIMARY KEY AUTOINCREMENT,
        POId INT NOT NULL,
        LineNumber INT NOT NULL,
        ItemId INT NULL,
        ItemCode NVARCHAR(100) NOT NULL,
        Description NVARCHAR(200) NULL,
        Quantity DECIMAL(18,4) NOT NULL,
        UnitPrice DECIMAL(18,4) NOT NULL,
        CONSTRAINT UQ_PurchaseOrderLines UNIQUE (POId, LineNumber),
        CONSTRAINT FK_PurchaseOrderLines_PO FOREIGN KEY (POId) REFERENCES PurchaseOrders(POId),
        CONSTRAINT FK_PurchaseOrderLines_Item FOREIGN KEY (ItemId) REFERENCES Items(ItemId)
    );''',
    '''CREATE TABLE IF NOT EXISTS SalesOrders (
        SOId INTEGER PRIMARY KEY AUTOINCREMENT,
        SONumber VARCHAR(100) NOT NULL,
        CustomerId INT NOT NULL,
        SODate DATE NOT NULL,
        Status VARCHAR(30) NOT NULL DEFAULT 'Open',
        SiteId INT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        CONSTRAINT UQ_SalesOrders_Number UNIQUE (SONumber),
        CONSTRAINT FK_SalesOrders_Customer FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId),
        CONSTRAINT FK_SalesOrders_Site FOREIGN KEY (SiteId) REFERENCES Sites(SiteId)
    );''',
    '''CREATE TABLE IF NOT EXISTS SalesOrderLines (
        SOLineId INTEGER PRIMARY KEY AUTOINCREMENT,
        SOId INT NOT NULL,
        LineNumber INT NOT NULL,
        ItemId INT NULL,
        ItemCode NVARCHAR(100) NOT NULL,
        Description NVARCHAR(200) NULL,
        Quantity DECIMAL(18,4) NOT NULL,
        UnitPrice DECIMAL(18,4) NOT NULL,
        CONSTRAINT UQ_SalesOrderLines UNIQUE (SOId, LineNumber),
        CONSTRAINT FK_SalesOrderLines_SO FOREIGN KEY (SOId) REFERENCES SalesOrders(SOId),
        CONSTRAINT FK_SalesOrderLines_Item FOREIGN KEY (ItemId) REFERENCES Items(ItemId)
    );''',
    '''CREATE TABLE IF NOT EXISTS AssetTransactions (
        AssetTxnId INTEGER PRIMARY KEY AUTOINCREMENT,
        AssetId INT NOT NULL,
        FromLocationId INT NULL,
        ToLocationId INT NULL,
        TxnType VARCHAR(30) NOT NULL,
        Quantity INT NOT NULL DEFAULT 1,
        TxnDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        Note NVARCHAR(500) NULL,
        CONSTRAINT FK_AssetTransactions_Asset FOREIGN KEY (AssetId) REFERENCES Assets(AssetId),
        CONSTRAINT FK_AssetTransactions_FromLoc FOREIGN KEY (FromLocationId) REFERENCES Locations(LocationId),
        CONSTRAINT FK_AssetTransactions_ToLoc FOREIGN KEY (ToLocationId) REFERENCES Locations(LocationId)
    );'''
]
import sqlite3

def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    for table_sql in db_schema:
        cursor.execute(table_sql)

    conn.commit()
    conn.close()
    print("Database 'inventory.db' initialized with sample data.")

if __name__ == "__main__":
    init_db()