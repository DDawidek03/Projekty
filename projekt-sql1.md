# 🏦 SalesDB - System Analityczny dla Globalnej Korporacji E-commerce i Bankowości

## 📋 Opis projektu

Baza danych **SalesDB** stanowi fundament kompleksowego systemu analitycznego przeznaczonego dla fikcyjnej globalnej korporacji zarządzającej sklepami internetowymi oraz operacjami bankowymi. System umożliwia zbieranie, przetwarzanie i analizę danych sprzedażowych oraz bankowych w czasie rzeczywistym.

## 🎯 Cele projektu

Celem projektu jest stworzenie kompletnego systemu analitycznego umożliwiającego:

- Pobieranie, oczyszczanie i przechowywanie danych sprzedażowych oraz bankowych
- Wizualizację i analizę danych w czasie rzeczywistym
- Wspieranie decyzji biznesowych na podstawie zgromadzonych danych

## 🗄️ Struktura bazy danych

Baza danych składa się z następujących tabel, które wspólnie tworzą kompletny model danych dla procesów e-commerce i bankowości:

### 🛒 Moduł sprzedażowy (E-commerce)

- **Products** - produkty dostępne w sprzedaży
- **Categories** - kategorie produktów z hierarchiczną strukturą
- **Customers** - dane klientów
- **Orders** - zamówienia klientów
- **OrderDetails** - szczegóły poszczególnych zamówień
- **Promotions** - promocje i oferty specjalne

### 💰 Moduł bankowy

- **BankAccounts** - konta bankowe sprzedawców
- **BankTransactions** - transakcje bankowe

### 🌍 Moduł geograficzny

- **Countries** - kraje działalności
- **Regions** - regiony w ramach krajów

### 👥 Moduł zarządzania

- **Sellers** - sprzedawcy i pracownicy

### 📅 Wymiar czasu

- **DateDimension** - wymiar czasowy dla analiz

## 📊 Diagram ERD

![Diagram ERD bazy danych SalesDB](SalesDB_ERD.png)

## 🔄 Proces przetwarzania danych

Baza SalesDB jest elementem większego ekosystemu analitycznego:

1. **Źródła danych** → Dane strukturyzowane (transakcje) i niestrukturyzowane (historie zakupów)
2. **Przechowywanie** → MS SQL Server (dane strukturyzowane) i MongoDB (dane elastyczne)
3. **Oczyszczanie** → Python, Power Query (dane bankowe) i Azure Data Factory (dane sprzedażowe)
4. **Magazynowanie** → Azure SQL Database i Azure Cosmos DB
5. **Wizualizacja** → Power BI

## 💻 Kod SQL

Kompletny kod SQL tworzący strukturę bazy danych oraz wszystkie zapytania znajduje się w pliku [**SalesDB.sql**](./SalesDB.sql).

## 🚀 Rozszerzenia i integracje

Baza danych SalesDB została zaprojektowana z myślą o:

- Optymalizacji pod kątem wysokiej wydajności w MS SQL Server
- Łatwej integracji z MongoDB dla przechowywania elastycznych struktur danych
- Bezproblemowej migracji do chmury Azure (Azure SQL Database)
- Współpracy z narzędziami Business Intelligence (Power BI)

## 📈 Przykładowe zapytania analityczne

```sql
-- Analiza sprzedaży według kategorii produktów
SELECT c.CategoryName, SUM(od.Quantity * od.UnitPrice) AS TotalSales
FROM OrderDetails od
JOIN Products p ON od.ProductID = p.ProductID
JOIN Categories c ON p.CategoryID = c.CategoryID
GROUP BY c.CategoryName
ORDER BY TotalSales DESC;

-- Analiza transakcji bankowych według regionów
SELECT r.RegionName, SUM(bt.Amount) AS TotalTransactions
FROM BankTransactions bt
JOIN BankAccounts ba ON bt.AccountID = ba.AccountID
JOIN Sellers s ON ba.SellerID = s.SellerID
JOIN Regions r ON s.RegionID = r.RegionID
GROUP BY r.RegionName
ORDER BY TotalTransactions DESC;
```

---

> Autor: Damian Dawidek
