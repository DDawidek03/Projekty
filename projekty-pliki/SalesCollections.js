// Tworzenie kolekcji MongoDB i walidacja schematów

// Kolekcja Historie Zakupów
db.createCollection("PurchaseHistories", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "CustomerID",
        "Email",
        "CountryID",
        "Purchases",
        "LastUpdated",
      ],
      properties: {
        CustomerID: { bsonType: "int" },
        Email: { bsonType: "string" },
        CountryID: { bsonType: "int" },
        Purchases: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: [
              "OrderID",
              "OrderDate",
              "Year",
              "Quarter",
              "Month",
              "TotalAmount",
              "Status",
              "Seller",
              "Products",
              "ShippingCountryID",
              "PaymentMethod",
            ],
            properties: {
              OrderID: { bsonType: "int" },
              OrderDate: { bsonType: "date" },
              Year: { bsonType: "int" },
              Quarter: { bsonType: "int" },
              Month: { bsonType: "int" },
              TotalAmount: { bsonType: "double" },
              Status: { bsonType: "string" },
              Seller: {
                bsonType: "object",
                required: ["SellerID", "SellerName", "SellerType", "RegionID"],
                properties: {
                  SellerID: { bsonType: "int" },
                  SellerName: { bsonType: "string" },
                  SellerType: { bsonType: "string" },
                  RegionID: { bsonType: "int" },
                },
              },
              Products: {
                bsonType: "array",
                items: {
                  bsonType: "object",
                  required: [
                    "ProductID",
                    "ProductName",
                    "CategoryID",
                    "CategoryName",
                    "Quantity",
                    "UnitPrice",
                    "UnitCostPrice",
                    "Discount",
                  ],
                  properties: {
                    ProductID: { bsonType: "int" },
                    ProductName: { bsonType: "string" },
                    CategoryID: { bsonType: "int" },
                    CategoryName: { bsonType: "string" },
                    Quantity: { bsonType: "int" },
                    UnitPrice: { bsonType: "double" },
                    UnitCostPrice: { bsonType: "double" },
                    Discount: { bsonType: "double" },
                  },
                },
              },
              ShippingCountryID: { bsonType: "int" },
              PaymentMethod: { bsonType: "string" },
            },
          },
        },
        LastUpdated: { bsonType: "date" },
      },
    },
  },
});

// Kolekcja Logi Transakcji Bankowych
db.createCollection("BankTransactionLogs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "AccountID",
        "AccountNumber",
        "Currency",
        "Transactions",
        "LastUpdated",
      ],
      properties: {
        AccountID: { bsonType: "int" },
        AccountNumber: { bsonType: "string" },
        Currency: { bsonType: "string" },
        Transactions: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: [
              "TransactionID",
              "TransactionDate",
              "Year",
              "Quarter",
              "Month",
              "Amount",
              "TransactionType",
              "Status",
              "Seller",
            ],
            properties: {
              TransactionID: { bsonType: "int" },
              TransactionDate: { bsonType: "date" },
              Year: { bsonType: "int" },
              Quarter: { bsonType: "int" },
              Month: { bsonType: "int" },
              Amount: { bsonType: "double" },
              TransactionType: { bsonType: "string" },
              Description: { bsonType: "string" },
              Counterparty: { bsonType: "string" },
              ReferenceNumber: { bsonType: "string" },
              Status: { bsonType: "string" },
              Seller: {
                bsonType: "object",
                required: ["SellerID", "SellerName", "SellerType", "RegionID"],
                properties: {
                  SellerID: { bsonType: "int" },
                  SellerName: { bsonType: "string" },
                  SellerType: { bsonType: "string" },
                  RegionID: { bsonType: "int" },
                },
              },
            },
          },
        },
        LastUpdated: { bsonType: "date" },
      },
    },
  },
});

// Kolekcja Dane Behawioralne
db.createCollection("CustomerBehavior", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["CustomerID", "Email", "CountryID", "Activity", "LastUpdated"],
      properties: {
        CustomerID: { bsonType: "int" },
        Email: { bsonType: "string" },
        CountryID: { bsonType: "int" },
        Activity: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: [
              "EventID",
              "EventType",
              "EventDate",
              "Year",
              "Quarter",
              "Month",
              "Details",
            ],
            properties: {
              EventID: { bsonType: "int" },
              EventType: { bsonType: "string" },
              EventDate: { bsonType: "date" },
              Year: { bsonType: "int" },
              Quarter: { bsonType: "int" },
              Month: { bsonType: "int" },
              Details: {
                bsonType: "object",
                required: [
                  "ProductID",
                  "ProductName",
                  "CategoryID",
                  "CategoryName",
                  "Action",
                  "PageURL",
                  "SessionID",
                  "SellerID",
                  "SellerName",
                  "RegionID",
                ],
                properties: {
                  ProductID: { bsonType: "int" },
                  ProductName: { bsonType: "string" },
                  CategoryID: { bsonType: "int" },
                  CategoryName: { bsonType: "string" },
                  Action: { bsonType: "string" },
                  PageURL: { bsonType: "string" },
                  SessionID: { bsonType: "string" },
                  SellerID: { bsonType: "int" },
                  SellerName: { bsonType: "string" },
                  RegionID: { bsonType: "int" },
                },
              },
            },
          },
        },
        LastUpdated: { bsonType: "date" },
      },
    },
  },
});

// Kolekcja Profile Sprzedawców
db.createCollection("SellerProfiles", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "SellerID",
        "Email",
        "FirstName",
        "LastName",
        "SellerType",
        "RegionID",
        "HireDate",
        "Products",
        "SalesSummary",
        "LastUpdated",
      ],
      properties: {
        SellerID: { bsonType: "int" },
        Email: { bsonType: "string" },
        FirstName: { bsonType: "string" },
        LastName: { bsonType: "string" },
        SellerType: { bsonType: "string" },
        RegionID: { bsonType: "int" },
        HireDate: { bsonType: "date" },
        Products: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: [
              "ProductID",
              "ProductName",
              "CategoryID",
              "CategoryName",
              "Price",
              "CostPrice",
            ],
            properties: {
              ProductID: { bsonType: "int" },
              ProductName: { bsonType: "string" },
              CategoryID: { bsonType: "int" },
              CategoryName: { bsonType: "string" },
              Price: { bsonType: "double" },
              CostPrice: { bsonType: "double" },
            },
          },
        },
        SalesSummary: {
          bsonType: "object",
          required: [
            "TotalOrders",
            "TotalRevenue",
            "AverageOrderValue",
            "TotalProductsSold",
          ],
          properties: {
            TotalOrders: { bsonType: "int" },
            TotalRevenue: { bsonType: "double" },
            AverageOrderValue: { bsonType: "double" },
            TotalProductsSold: { bsonType: "int" },
          },
        },
        LastUpdated: { bsonType: "date" },
      },
    },
  },
});
