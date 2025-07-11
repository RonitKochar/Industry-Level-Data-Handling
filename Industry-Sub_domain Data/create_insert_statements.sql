CREATE TABLE Artists (
    ArtistID INT PRIMARY KEY,
    Name VARCHAR(100),
    Genre VARCHAR(50),
    Country VARCHAR(50),
    DebutYear INT
);

CREATE TABLE Albums (
    AlbumID INT PRIMARY KEY,
    Title VARCHAR(100),
    ReleaseDate DATE,
    ArtistID INT,
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID)
);

CREATE TABLE Tracks (
    TrackID INT PRIMARY KEY,
    Title VARCHAR(100),
    Duration INT,
    AlbumID INT,
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID)
);

CREATE TABLE Sales (
    SaleID INT PRIMARY KEY,
    AlbumID INT,
    Quantity INT,
    SaleDate DATE,
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID)
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Country VARCHAR(50),
    SignUpDate DATE
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT,
    TrackID INT,
    Quantity INT,
    Price DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (TrackID) REFERENCES Tracks(TrackID)
);

CREATE TABLE Genres (
    GenreID INT PRIMARY KEY,
    Name VARCHAR(50)
);

CREATE TABLE ArtistGenres (
    ArtistID INT,
    GenreID INT,
    PRIMARY KEY (ArtistID, GenreID),
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID),
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
);

CREATE TABLE Reviews (
    ReviewID INT PRIMARY KEY,
    AlbumID INT,
    CustomerID INT,
    Rating INT,
    ReviewText TEXT,
    ReviewDate DATE,
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

INSERT INTO Artists (ArtistID, Name, Genre, Country, DebutYear) VALUES
(1, 'Taylor Swift', 'Pop', 'USA', 2006),
(2, 'Ed Sheeran', 'Pop', 'UK', 2011),
(3, 'Beyonce', 'R&B', 'USA', 1997),
(4, 'Taylr Swft', 'Pop', 'USA', 2006),
(5, 'Adele', 'Pop', 'UK', 2008),
(6, 'Drake', 'Hip-Hop', 'Canada', 2006),
(7, 'Justin Bieber', 'Pop', 'Canada', 2009),
(8, 'Rihanna', 'Pop', 'Barbados', 2005),
(9, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'Unknown', 'Unknown', 1900),
(10, NULL, 'Experimental', 'XX', NULL);

INSERT INTO Albums (AlbumID, Title, ReleaseDate, ArtistID) VALUES
(1, 'Fearless', '2008-11-11', 1),
(2, 'Divide', '2017-03-03', 2),
(3, 'Lemonade', '2016-04-23', 3),
(4, 'Red', '2012-10-22', 1),
(5, '21', '2011-01-24', 5),
(6, 'Scorpion', '2018-06-29', 6),
(7, 'Purpose', '2015-11-13', 7),
(8, 'Anti', '2016-01-28', 8),
(9, '1989', '2014-10-27', 1),
(10, 'Unknown Album', '2099-12-31', 9);

INSERT INTO Tracks (TrackID, Title, Duration, AlbumID) VALUES
(1, 'Love Story', 247, 1),
(2, 'Shape of You', 234, 2),
(3, 'Hold Up', 210, 3),
(4, 'All Too Well', 336, 4),
(5, 'Rolling in the Deep', 232, 5),
(6, 'God\'s Plan', 220, 6),
(7, 'Sorry', 224, 7),
(8, 'Work', 220, 8),
(9, 'Blank Space', 242, 9),
(10, 'Track with 0 Duration', 0, 10);

INSERT INTO Sales (SaleID, AlbumID, Quantity, SaleDate) VALUES
(1, 1, 500, '2023-01-15'),
(2, 2, 700, '2023-02-20'),
(3, 3, 600, '2023-03-25'),
(4, 4, 450, '2023-04-30'),
(5, 5, 800, '2023-05-10'),
(6, 6, 900, '2023-06-15'),
(7, 7, 550, '2023-07-20'),
(8, 8, 650, '2023-08-25'),
(9, 9, -100, '2023-09-30'),
(10, 10, NULL, '1900-01-01');

INSERT INTO Customers (CustomerID, Name, Email, Country, SignUpDate) VALUES
(1, 'John Doe', 'john.doe@example.com', 'USA', '2022-01-10'),
(2, 'Jane Smith', 'jane.smith@example.com', 'UK', '2022-02-15'),
(3, 'Alice Johnson', 'alice.johnson@example.com', 'Canada', '2022-03-20'),
(4, 'Bob Brown', 'bob.brown@example.com', 'Australia', '2022-04-25'),
(5, 'Charlie Davis', 'charlie.davis@example.com', 'Germany', '2022-05-30'),
(6, 'Eve Wilson', 'eve.wilson@example.com', 'France', '2022-06-05'),
(7, 'Frank Miller', 'frank.miller@example.com', 'Japan', '2022-07-10'),
(8, 'Grace Lee', 'grace.lee@example.com', 'South Korea', '2022-08-15'),
(9, 'Harry Potter', 'harry.potter@example.com', 'XX', '2022-09-20'),
(10, NULL, 'unknown@example.com', 'Unknown', NULL);

INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount) VALUES
(1, 1, '2023-01-10', 29.99),
(2, 2, '2023-02-15', 39.99),
(3, 3, '2023-03-20', 49.99),
(4, 4, '2023-04-25', 59.99),
(5, 5, '2023-05-30', 69.99),
(6, 6, '2023-06-05', 79.99),
(7, 7, '2023-07-10', 89.99),
(8, 8, '2023-08-15', 99.99),
(9, 9, '2023-09-20', 999999.99),
(10, 10, '2023-10-25', NULL);

INSERT INTO OrderDetails (OrderDetailID, OrderID, TrackID, Quantity, Price) VALUES
(1, 1, 1, 1, 9.99),
(2, 2, 2, 1, 10.99),
(3, 3, 3, 1, 11.99),
(4, 4, 4, 1, 12.99),
(5, 5, 5, 1, 13.99),
(6, 6, 6, 1, 14.99),
(7, 7, 7, 1, 15.99),
(8, 8, 8, 1, 16.99),
(9, 9, 9, 1, 17.99),
(10, 10, 10, 1, NULL);

INSERT INTO Genres (GenreID, Name) VALUES
(1, 'Pop'),
(2, 'Rock'),
(3, 'Jazz'),
(4, 'Hip-Hop'),
(5, 'Classical'),
(6, 'Country'),
(7, 'Electronic'),
(8, 'R&B'),
(9, 'Folk'),
(10, 'Experimental');

INSERT INTO ArtistGenres (ArtistID, GenreID) VALUES
(1, 1),
(2, 1),
(3, 8),
(4, 1),
(5, 1),
(6, 4),
(7, 1),
(8, 8),
(9, 10),
(10, NULL);

INSERT INTO Reviews (ReviewID, AlbumID, CustomerID, Rating, ReviewText, ReviewDate) VALUES
(1, 1, 1, 5, 'Great album!', '2023-01-12'),
(2, 2, 2, 4, 'Loved it!', '2023-02-17'),
(3, 3, 3, 5, 'Amazing songs!', '2023-03-22'),
(4, 4, 4, 4, 'Good tracks.', '2023-04-27'),
(5, 5, 5, 5, 'Best album ever!', '2023-05-02'),
(6, 6, 6, 4, 'Nice beats.', '2023-06-07'),
(7, 7, 7, 3, 'Decent album.', '2023-07-12'),
(8, 8, 8, 5, 'Loved every song!', '2023-08-17'),
(9, 9, 9, 1, 'Worst album ever!', '2023-09-22'),
(10, 10, 10, NULL, 'This is a review text that is excessively long and should not be allowed in a real-world scenario. It is meant to simulate a data entry error or an outlier in the dataset.', '2023-10-27');