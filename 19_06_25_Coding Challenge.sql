CREATE DATABASE IF NOT EXISTS PetPals;
USE PetPals;

CREATE TABLE Shelters (
    ShelterID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Location VARCHAR(255)
);

CREATE TABLE Pets (
    PetID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Age INT,
    Breed VARCHAR(100),
    Type VARCHAR(50),
    AvailableForAdoption BIT DEFAULT 1,
    OwnerID INT,
    ShelterID INT,
    FOREIGN KEY (ShelterID) REFERENCES Shelters(ShelterID)
);


CREATE TABLE Donations (
    DonationID INT PRIMARY KEY AUTO_INCREMENT,
    DonorName VARCHAR(100),
    DonationType VARCHAR(50),
    DonationAmount DECIMAL(10, 2),
    DonationItem VARCHAR(100),
    DonationDate DATETIME,
    ShelterID INT,
    FOREIGN KEY (ShelterID) REFERENCES Shelters(ShelterID)
);


CREATE TABLE AdoptionEvents (
    EventID INT PRIMARY KEY AUTO_INCREMENT,
    EventName VARCHAR(100),
    EventDate DATETIME,
    Location VARCHAR(255)
);


CREATE TABLE Participants (
    ParticipantID INT PRIMARY KEY AUTO_INCREMENT,
    ParticipantName VARCHAR(100),
    ParticipantType VARCHAR(50),
    EventID INT,
    FOREIGN KEY (EventID) REFERENCES AdoptionEvents(EventID)
);

CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Name VARCHAR(100)
);

INSERT INTO Shelters (Name, Location) VALUES
('Happy Tails Shelter', 'Chennai'),
('SafePaws Rescue', 'Bangalore'),
('Whisker Haven', 'Mumbai');

INSERT INTO Pets (Name, Age, Breed, Type, AvailableForAdoption, OwnerID, ShelterID) VALUES
('Buddy', 2, 'Labrador', 'Dog', 1, NULL, 1),
('Milo', 1, 'Beagle', 'Dog', 1, NULL, 1),
('Whiskers', 6, 'Persian', 'Cat', 1, NULL, 2),
('Max', 4, 'Labrador', 'Dog', 0, 101, 1),
('Coco', 5, 'Siamese', 'Cat', 1, NULL, 3),
('Shadow', 7, 'German Shepherd', 'Dog', 0, 102, 2),
('Fluffy', 3, 'Persian', 'Cat', 1, NULL, 2);

INSERT INTO Donations (DonorName, DonationType, DonationAmount, DonationItem, DonationDate, ShelterID) VALUES
('Anjali Mehra', 'Cash', 5000.00, NULL, '2023-01-15 10:00:00', 1),
('Rahul Verma', 'Item', NULL, 'Dog Food', '2023-02-10 14:30:00', 2),
('Sita Rao', 'Cash', 3000.00, NULL, '2023-01-22 11:15:00', 1),
('Ravi Kumar', 'Cash', 7000.00, NULL, '2023-03-05 09:45:00', 3),
('Leena Shah', 'Item', NULL, 'Cat Toys', '2023-03-18 16:00:00', 1);

INSERT INTO AdoptionEvents (EventName, EventDate, Location) VALUES
('PawFest 2023', '2023-04-10 11:00:00', 'Chennai'),
('Adoptathon', '2023-05-05 09:00:00', 'Bangalore');

INSERT INTO Participants (ParticipantName, ParticipantType, EventID) VALUES
('Happy Tails Shelter', 'Shelter', 1),
('SafePaws Rescue', 'Shelter', 2),
('John Doe', 'Adopter', 1),
('Meena Kumari', 'Adopter', 2),
('Whisker Haven', 'Shelter', 1);

INSERT INTO Users (UserID, Name) VALUES
(101, 'John Doe'),
(102, 'Meena Kumari');

SELECT Name, Age, Breed, Type
FROM Pets
WHERE AvailableForAdoption = TRUE;

SELECT ParticipantName, ParticipantType FROM Participants WHERE EventID = 1;

DELIMITER //

CREATE PROCEDURE UpdateShelterInfo(
    IN p_ShelterID INT,
    IN p_Name VARCHAR(100),
    IN p_Location VARCHAR(255)
)
BEGIN
    IF EXISTS (SELECT 1 FROM Shelters WHERE ShelterID = p_ShelterID) THEN
        UPDATE Shelters
        SET Name = p_Name, Location = p_Location
        WHERE ShelterID = p_ShelterID;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Shelter ID not found.';
    END IF;
END //

DELIMITER ;

SELECT s.Name AS ShelterName, COALESCE(SUM(d.DonationAmount), 0) AS TotalDonations
FROM Shelters s
LEFT JOIN Donations d ON s.ShelterID = d.ShelterID
GROUP BY s.ShelterID;

SELECT Name, Age, Breed, Type FROM Pets WHERE OwnerID IS NULL;

SELECT DATE_FORMAT(DonationDate, '%M %Y') AS MonthYear,
       SUM(DonationAmount) AS TotalDonation
FROM Donations
GROUP BY DATE_FORMAT(DonationDate, '%M %Y');	

SELECT DISTINCT Breed FROM Pets WHERE (Age BETWEEN 1 AND 3) OR (Age > 5);

SELECT p.Name AS PetName, s.Name AS ShelterName
FROM Pets p
JOIN Shelters s ON p.ShelterID = s.ShelterID
WHERE p.AvailableForAdoption = 1;

SELECT COUNT(p.ParticipantID) AS TotalParticipants
FROM Participants p
JOIN AdoptionEvents e ON p.EventID = e.EventID
JOIN Shelters s ON p.ParticipantType = 'Shelter' AND p.ParticipantName = s.Name
WHERE s.Location = 'Chennai';

SELECT DISTINCT Breed FROM Pets WHERE Age BETWEEN 1 AND 5;

SELECT * FROM Pets WHERE OwnerID IS NULL;

SELECT p.Name AS PetName, u.Name AS AdopterName
FROM Pets p
JOIN Users u ON p.OwnerID = u.UserID;

SELECT s.Name AS ShelterName, COUNT(p.PetID) AS AvailablePets
FROM Shelters s
LEFT JOIN Pets p ON s.ShelterID = p.ShelterID AND p.AvailableForAdoption = 1
GROUP BY s.ShelterID;

SELECT p1.Name AS Pet1, p2.Name AS Pet2, p1.Breed, s.Name AS ShelterName
FROM Pets p1
JOIN Pets p2 ON p1.Breed = p2.Breed AND p1.PetID < p2.PetID AND p1.ShelterID = p2.ShelterID
JOIN Shelters s ON p1.ShelterID = s.ShelterID;

SELECT s.Name AS ShelterName, e.EventName
FROM Shelters s
CROSS JOIN AdoptionEvents e;

SELECT s.Name, COUNT(p.PetID) AS AdoptedPets
FROM Pets p
JOIN Shelters s ON p.ShelterID = s.ShelterID
WHERE p.OwnerID IS NOT NULL
GROUP BY s.ShelterID
ORDER BY AdoptedPets DESC
LIMIT 1;




