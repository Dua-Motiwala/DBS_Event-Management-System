
/* =========================================================
   USERS TABLE
   Stores all system users (Admin, Organizer, Attendee)
   Role column defines permissions
========================================================= */
CREATE TABLE Users (
    UserID NUMBER PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL,
    Email VARCHAR2(100) UNIQUE NOT NULL,
    Password VARCHAR2(100) NOT NULL,
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
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
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