-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Czas generowania: 17 Kwi 2025, 17:48
-- Wersja serwera: 5.7.39
-- Wersja PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `SalesDB`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `BankAccounts`
--

CREATE TABLE `BankAccounts` (
  `AccountID` int(11) NOT NULL,
  `AccountNumber` varchar(50) DEFAULT NULL,
  `BankName` varchar(100) DEFAULT NULL,
  `Currency` varchar(3) DEFAULT NULL,
  `Balance` decimal(15,2) DEFAULT NULL,
  `AccountType` varchar(20) DEFAULT NULL,
  `SellerID` int(11) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `BankTransactions`
--

CREATE TABLE `BankTransactions` (
  `TransactionID` int(11) NOT NULL,
  `AccountID` int(11) DEFAULT NULL,
  `TransactionDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `DateID` int(11) DEFAULT NULL,
  `Amount` decimal(15,2) DEFAULT NULL,
  `TransactionType` varchar(20) DEFAULT NULL,
  `Description` varchar(200) DEFAULT NULL,
  `Counterparty` varchar(100) DEFAULT NULL,
  `ReferenceNumber` varchar(50) DEFAULT NULL,
  `SellerID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Categories`
--

CREATE TABLE `Categories` (
  `CategoryID` int(11) NOT NULL,
  `CategoryName` varchar(50) DEFAULT NULL,
  `ParentCategoryID` int(11) DEFAULT NULL,
  `Description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Countries`
--

CREATE TABLE `Countries` (
  `CountryID` int(11) NOT NULL,
  `CountryName` varchar(50) DEFAULT NULL,
  `Continent` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Customers`
--

CREATE TABLE `Customers` (
  `CustomerID` int(11) NOT NULL,
  `FirstName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `CountryID` int(11) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `DateDimension`
--

CREATE TABLE `DateDimension` (
  `DateID` int(11) NOT NULL,
  `FullDate` date DEFAULT NULL,
  `Year` int(11) DEFAULT NULL,
  `Quarter` int(11) DEFAULT NULL,
  `Month` int(11) DEFAULT NULL,
  `MonthName` varchar(20) DEFAULT NULL,
  `Day` int(11) DEFAULT NULL,
  `DayOfWeek` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `OrderDetails`
--

CREATE TABLE `OrderDetails` (
  `OrderDetailID` int(11) NOT NULL,
  `OrderID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `UnitPrice` decimal(10,2) DEFAULT NULL,
  `UnitCostPrice` decimal(10,2) DEFAULT NULL,
  `Discount` decimal(5,2) DEFAULT '0.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Orders`
--

CREATE TABLE `Orders` (
  `OrderID` int(11) NOT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `SellerID` int(11) DEFAULT NULL,
  `OrderDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `DateID` int(11) DEFAULT NULL,
  `TotalAmount` decimal(10,2) DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL,
  `ShippingAddress` varchar(200) DEFAULT NULL,
  `CountryID` int(11) DEFAULT NULL,
  `PaymentMethod` varchar(50) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Products`
--

CREATE TABLE `Products` (
  `ProductID` int(11) NOT NULL,
  `ProductName` varchar(100) DEFAULT NULL,
  `CategoryID` int(11) DEFAULT NULL,
  `SellerID` int(11) DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `CostPrice` decimal(10,2) DEFAULT NULL,
  `StockQuantity` int(11) DEFAULT NULL,
  `Description` varchar(500) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Promotions`
--

CREATE TABLE `Promotions` (
  `PromotionID` int(11) NOT NULL,
  `PromotionName` varchar(100) DEFAULT NULL,
  `StartDateID` int(11) DEFAULT NULL,
  `EndDateID` int(11) DEFAULT NULL,
  `DiscountPercentage` decimal(5,2) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `CategoryID` int(11) DEFAULT NULL,
  `SellerID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Regions`
--

CREATE TABLE `Regions` (
  `RegionID` int(11) NOT NULL,
  `RegionName` varchar(50) DEFAULT NULL,
  `CountryID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Sellers`
--

CREATE TABLE `Sellers` (
  `SellerID` int(11) NOT NULL,
  `FirstName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `SellerType` varchar(20) DEFAULT NULL,
  `RegionID` int(11) DEFAULT NULL,
  `HireDate` datetime DEFAULT NULL,
  `CreatedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `UpdatedAt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `BankAccounts`
--
ALTER TABLE `BankAccounts`
  ADD PRIMARY KEY (`AccountID`),
  ADD UNIQUE KEY `AccountNumber` (`AccountNumber`),
  ADD KEY `SellerID` (`SellerID`);

--
-- Indeksy dla tabeli `BankTransactions`
--
ALTER TABLE `BankTransactions`
  ADD PRIMARY KEY (`TransactionID`),
  ADD KEY `AccountID` (`AccountID`),
  ADD KEY `DateID` (`DateID`),
  ADD KEY `SellerID` (`SellerID`);

--
-- Indeksy dla tabeli `Categories`
--
ALTER TABLE `Categories`
  ADD PRIMARY KEY (`CategoryID`),
  ADD KEY `ParentCategoryID` (`ParentCategoryID`);

--
-- Indeksy dla tabeli `Countries`
--
ALTER TABLE `Countries`
  ADD PRIMARY KEY (`CountryID`);

--
-- Indeksy dla tabeli `Customers`
--
ALTER TABLE `Customers`
  ADD PRIMARY KEY (`CustomerID`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `CountryID` (`CountryID`);

--
-- Indeksy dla tabeli `DateDimension`
--
ALTER TABLE `DateDimension`
  ADD PRIMARY KEY (`DateID`);

--
-- Indeksy dla tabeli `OrderDetails`
--
ALTER TABLE `OrderDetails`
  ADD PRIMARY KEY (`OrderDetailID`),
  ADD KEY `OrderID` (`OrderID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indeksy dla tabeli `Orders`
--
ALTER TABLE `Orders`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `CustomerID` (`CustomerID`),
  ADD KEY `SellerID` (`SellerID`),
  ADD KEY `DateID` (`DateID`),
  ADD KEY `CountryID` (`CountryID`);

--
-- Indeksy dla tabeli `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`ProductID`),
  ADD KEY `CategoryID` (`CategoryID`),
  ADD KEY `SellerID` (`SellerID`);

--
-- Indeksy dla tabeli `Promotions`
--
ALTER TABLE `Promotions`
  ADD PRIMARY KEY (`PromotionID`),
  ADD KEY `StartDateID` (`StartDateID`),
  ADD KEY `EndDateID` (`EndDateID`),
  ADD KEY `ProductID` (`ProductID`),
  ADD KEY `CategoryID` (`CategoryID`),
  ADD KEY `SellerID` (`SellerID`);

--
-- Indeksy dla tabeli `Regions`
--
ALTER TABLE `Regions`
  ADD PRIMARY KEY (`RegionID`),
  ADD KEY `CountryID` (`CountryID`);

--
-- Indeksy dla tabeli `Sellers`
--
ALTER TABLE `Sellers`
  ADD PRIMARY KEY (`SellerID`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `RegionID` (`RegionID`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `BankAccounts`
--
ALTER TABLE `BankAccounts`
  MODIFY `AccountID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `BankTransactions`
--
ALTER TABLE `BankTransactions`
  MODIFY `TransactionID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `Categories`
--
ALTER TABLE `Categories`
  MODIFY `CategoryID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `Countries`
--
ALTER TABLE `Countries`
  MODIFY `CountryID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `Customers`
--
ALTER TABLE `Customers`
  MODIFY `CustomerID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `DateDimension`
--
ALTER TABLE `DateDimension`
  MODIFY `DateID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `OrderDetails`
--
ALTER TABLE `OrderDetails`
  MODIFY `OrderDetailID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `Orders`
--
ALTER TABLE `Orders`
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `Products`
--
ALTER TABLE `Products`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `Promotions`
--
ALTER TABLE `Promotions`
  MODIFY `PromotionID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `Regions`
--
ALTER TABLE `Regions`
  MODIFY `RegionID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `Sellers`
--
ALTER TABLE `Sellers`
  MODIFY `SellerID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `BankAccounts`
--
ALTER TABLE `BankAccounts`
  ADD CONSTRAINT `bankaccounts_ibfk_1` FOREIGN KEY (`SellerID`) REFERENCES `Sellers` (`SellerID`);

--
-- Ograniczenia dla tabeli `BankTransactions`
--
ALTER TABLE `BankTransactions`
  ADD CONSTRAINT `banktransactions_ibfk_1` FOREIGN KEY (`AccountID`) REFERENCES `BankAccounts` (`AccountID`),
  ADD CONSTRAINT `banktransactions_ibfk_2` FOREIGN KEY (`DateID`) REFERENCES `DateDimension` (`DateID`),
  ADD CONSTRAINT `banktransactions_ibfk_3` FOREIGN KEY (`SellerID`) REFERENCES `Sellers` (`SellerID`);

--
-- Ograniczenia dla tabeli `Categories`
--
ALTER TABLE `Categories`
  ADD CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`ParentCategoryID`) REFERENCES `Categories` (`CategoryID`);

--
-- Ograniczenia dla tabeli `Customers`
--
ALTER TABLE `Customers`
  ADD CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`CountryID`) REFERENCES `Countries` (`CountryID`);

--
-- Ograniczenia dla tabeli `OrderDetails`
--
ALTER TABLE `OrderDetails`
  ADD CONSTRAINT `orderdetails_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `Orders` (`OrderID`),
  ADD CONSTRAINT `orderdetails_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `Products` (`ProductID`);

--
-- Ograniczenia dla tabeli `Orders`
--
ALTER TABLE `Orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customers` (`CustomerID`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`SellerID`) REFERENCES `Sellers` (`SellerID`),
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`DateID`) REFERENCES `DateDimension` (`DateID`),
  ADD CONSTRAINT `orders_ibfk_4` FOREIGN KEY (`CountryID`) REFERENCES `Countries` (`CountryID`);

--
-- Ograniczenia dla tabeli `Products`
--
ALTER TABLE `Products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`CategoryID`) REFERENCES `Categories` (`CategoryID`),
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`SellerID`) REFERENCES `Sellers` (`SellerID`);

--
-- Ograniczenia dla tabeli `Promotions`
--
ALTER TABLE `Promotions`
  ADD CONSTRAINT `promotions_ibfk_1` FOREIGN KEY (`StartDateID`) REFERENCES `DateDimension` (`DateID`),
  ADD CONSTRAINT `promotions_ibfk_2` FOREIGN KEY (`EndDateID`) REFERENCES `DateDimension` (`DateID`),
  ADD CONSTRAINT `promotions_ibfk_3` FOREIGN KEY (`ProductID`) REFERENCES `Products` (`ProductID`),
  ADD CONSTRAINT `promotions_ibfk_4` FOREIGN KEY (`CategoryID`) REFERENCES `Categories` (`CategoryID`),
  ADD CONSTRAINT `promotions_ibfk_5` FOREIGN KEY (`SellerID`) REFERENCES `Sellers` (`SellerID`);

--
-- Ograniczenia dla tabeli `Regions`
--
ALTER TABLE `Regions`
  ADD CONSTRAINT `regions_ibfk_1` FOREIGN KEY (`CountryID`) REFERENCES `Countries` (`CountryID`);

--
-- Ograniczenia dla tabeli `Sellers`
--
ALTER TABLE `Sellers`
  ADD CONSTRAINT `sellers_ibfk_1` FOREIGN KEY (`RegionID`) REFERENCES `Regions` (`RegionID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
