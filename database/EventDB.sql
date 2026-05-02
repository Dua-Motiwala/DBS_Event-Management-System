
/* =========================================================
   USERS TABLE
   Stores all system users (Admin, Organizer, Attendee)
   Role column defines permissions
========================================================= */
CREATE TABLE Users (
    UserID NUMBER PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL,
    Email VARCHAR2(100) UNIQUE NOT NULL,
    Password VARCHAR2(255) NOT NULL,
    Role VARCHAR2(20) CHECK (Role IN ('Admin','Organizer','Attendee'))
);

CREATE SEQUENCE users_seq;

CREATE OR REPLACE TRIGGER users_trg
BEFORE INSERT ON Users
FOR EACH ROW
BEGIN
    SELECT users_seq.NEXTVAL INTO :NEW.UserID FROM dual;
END;
/
------------------------------------------------------------


/* =========================================================
   VENUES TABLE
   Stores event locations (no user dependency)
========================================================= */
CREATE TABLE Venues (
    VenueID NUMBER PRIMARY KEY,
    Name VARCHAR2(100),
    Location VARCHAR2(100),
    Capacity NUMBER
);

CREATE SEQUENCE venues_seq;

CREATE OR REPLACE TRIGGER venues_trg
BEFORE INSERT ON Venues
FOR EACH ROW
BEGIN
    SELECT venues_seq.NEXTVAL INTO :NEW.VenueID FROM dual;
END;
/
------------------------------------------------------------


/* =========================================================
   CATEGORIES TABLE
   Defines event types (Sports, Seminar, Concert, etc.)
========================================================= */
CREATE TABLE Categories (
    CategoryID NUMBER PRIMARY KEY,
    CategoryName VARCHAR2(100)
);

CREATE SEQUENCE categories_seq;

CREATE OR REPLACE TRIGGER categories_trg
BEFORE INSERT ON Categories
FOR EACH ROW
BEGIN
    SELECT categories_seq.NEXTVAL INTO :NEW.CategoryID FROM dual;
END;
/
------------------------------------------------------------


/* =========================================================
   EVENTS TABLE
   Created by Users with Role = Organizer
   Links Venue, Category, and Organizer (UserID)
========================================================= */
CREATE TABLE Events (
    EventID NUMBER PRIMARY KEY,
    Title VARCHAR2(100),
    EventDate DATE,
    VenueID NUMBER,
    CategoryID NUMBER,
    UserID NUMBER,
    Status VARCHAR2(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Finished')),
    FOREIGN KEY (VenueID) REFERENCES Venues(VenueID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE SEQUENCE events_seq;

CREATE OR REPLACE TRIGGER events_trg
BEFORE INSERT ON Events
FOR EACH ROW
BEGIN
    SELECT events_seq.NEXTVAL INTO :NEW.EventID FROM dual;
END;
/

ALTER TABLE Events ADD (Status VARCHAR2(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Finished')));

------------------------------------------------------------


/* =========================================================
   REGISTRATIONS TABLE
   Attendees register for events using UserID
========================================================= */
CREATE TABLE Registrations (
    RegID NUMBER PRIMARY KEY,
    UserID NUMBER,
    EventID NUMBER,
    RegDate DATE DEFAULT SYSDATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    UNIQUE (UserID, EventID)
);

CREATE SEQUENCE reg_seq;

CREATE OR REPLACE TRIGGER reg_trg
BEFORE INSERT ON Registrations
FOR EACH ROW
BEGIN
    SELECT reg_seq.NEXTVAL INTO :NEW.RegID FROM dual;
END;
/
------------------------------------------------------------


/* =========================================================
   PAYMENTS TABLE
   Stores payments made by Users(Attendees) for Events
========================================================= */
CREATE TABLE Payments (
    PaymentID NUMBER PRIMARY KEY,
    UserID NUMBER,
    EventID NUMBER,
    Amount NUMBER(10,2),
    PaymentStatus VARCHAR2(20),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE SEQUENCE pay_seq;

CREATE OR REPLACE TRIGGER pay_trg
BEFORE INSERT ON Payments
FOR EACH ROW
BEGIN
    SELECT pay_seq.NEXTVAL INTO :NEW.PaymentID FROM dual;
END;
/
------------------------------------------------------------


/* =========================================================
   FEEDBACK TABLE
   Attendees give ratings and comments for events
========================================================= */
CREATE TABLE Feedback (
    FeedbackID NUMBER PRIMARY KEY,
    UserID NUMBER,
    EventID NUMBER,
    Rating NUMBER CHECK (Rating BETWEEN 1 AND 5),
    FeedbackText VARCHAR2(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE SEQUENCE feedback_seq;

CREATE OR REPLACE TRIGGER feedback_trg
BEFORE INSERT ON Feedback
FOR EACH ROW
BEGIN
    SELECT feedback_seq.NEXTVAL INTO :NEW.FeedbackID FROM dual;
END;
/
------------------------------------------------------------


/* =========================================================
   EVENT SCHEDULE TABLE
   Stores timing details of events
========================================================= */
CREATE TABLE Event_Schedule (
    ScheduleID NUMBER PRIMARY KEY,
    EventID NUMBER,
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE SEQUENCE schedule_seq;

CREATE OR REPLACE TRIGGER schedule_trg
BEFORE INSERT ON Event_Schedule
FOR EACH ROW
BEGIN
    SELECT schedule_seq.NEXTVAL INTO :NEW.ScheduleID FROM dual;
END;
/
------------------------------------------------------------


/* =========================================================
   ADMIN LOG TABLE
   Tracks actions performed by Admin users only
========================================================= */
CREATE TABLE Admin_Log (
    LogID NUMBER PRIMARY KEY,
    UserID NUMBER,
    Action VARCHAR2(255),
    ActionTime TIMESTAMP DEFAULT SYSTIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE SEQUENCE log_seq;

CREATE OR REPLACE TRIGGER log_trg
BEFORE INSERT ON Admin_Log
FOR EACH ROW
BEGIN
    SELECT log_seq.NEXTVAL INTO :NEW.LogID FROM dual;
END;
/
------------------------------------------------------------

ALTER TABLE Users MODIFY (Password VARCHAR2(255));

ALTER TABLE Registrations ADD CONSTRAINT unique_registration UNIQUE (UserID, EventID);


/* =========================================================
   VIEWS
   Requirement: Implement Views
========================================================= */

-- View that joins Events, Venues, and Categories (Requirement: Joins)
CREATE OR REPLACE VIEW vw_Event_Details AS
SELECT 
    e.EventID, 
    e.Title, 
    e.EventDate,
    e.Status,
    e.CategoryID, 
    v.Name AS VenueName, 
    v.Location, 
    c.CategoryName,
    u.Name AS OrganizerName
FROM Events e
JOIN Venues v ON e.VenueID = v.VenueID
JOIN Categories c ON e.CategoryID = c.CategoryID
JOIN Users u ON e.UserID = u.UserID;

-- View for Admin stats using built-in functions (Requirement: Built-in SQL functions)
CREATE OR REPLACE VIEW vw_Organizer_Stats AS
SELECT 
    u.UserID, 
    u.Name, 
    COUNT(e.EventID) AS TotalEvents,
    SUM(p.Amount) AS TotalRevenue
FROM Users u
LEFT JOIN Events e ON u.UserID = e.UserID
LEFT JOIN Payments p ON e.EventID = p.EventID
WHERE u.Role = 'Organizer'
GROUP BY u.UserID, u.Name;


/* =========================================================
   SUBPROGRAMS (PROCEDURES)
   Requirement: One program/subprogram for each user role
========================================================= */

-- 1. ADMIN SUBPROGRAM: Safely delete a user and related logs
CREATE OR REPLACE PROCEDURE sp_Delete_User(p_userid IN NUMBER) IS
BEGIN
    -- Transaction handling: Procedures often encapsulate logic
    DELETE FROM Admin_Log WHERE UserID = p_userid;
    DELETE FROM Users WHERE UserID = p_userid;
    COMMIT;
END;
/

-- 2. ORGANIZER SUBPROGRAM: Cancel an event (Delete operation)
CREATE OR REPLACE PROCEDURE sp_Cancel_Event(p_eventid IN NUMBER) IS
BEGIN
    -- Delete dependencies first
    DELETE FROM Event_Schedule WHERE EventID = p_eventid;
    DELETE FROM Registrations WHERE EventID = p_eventid;
    DELETE FROM Payments WHERE EventID = p_eventid;
    DELETE FROM Feedback WHERE EventID = p_eventid;
    DELETE FROM Events WHERE EventID = p_eventid;
    COMMIT;
END;
/

-- 3. ATTENDEE SUBPROGRAM: Handle event registration with validation
CREATE OR REPLACE PROCEDURE sp_Register_For_Event(
    p_userid IN NUMBER, 
    p_eventid IN NUMBER,
    p_status OUT VARCHAR2
) IS
    v_count NUMBER;
BEGIN
    -- Check if already registered
    SELECT COUNT(*) INTO v_count 
    FROM Registrations 
    WHERE UserID = p_userid AND EventID = p_eventid;
    
    IF v_count > 0 THEN
        p_status := 'ALREADY_REGISTERED';
    ELSE
        INSERT INTO Registrations (UserID, EventID, RegDate)
        VALUES (p_userid, p_eventid, SYSDATE);
        p_status := 'SUCCESS';
    END IF;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        p_status := 'ERROR: ' || SQLERRM;
        ROLLBACK;
END;
/

/*
BEGIN
   FOR t IN (SELECT table_name FROM user_tables) LOOP
      EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
   END LOOP;
END;
/

BEGIN
   FOR s IN (SELECT sequence_name FROM user_sequences) LOOP
      EXECUTE IMMEDIATE 'DROP SEQUENCE ' || s.sequence_name;
   END LOOP;
END;
/

BEGIN
   FOR tr IN (SELECT trigger_name FROM user_triggers) LOOP
      EXECUTE IMMEDIATE 'DROP TRIGGER ' || tr.trigger_name;
   END LOOP;
END;
/ */