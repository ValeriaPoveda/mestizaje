# Mestizaje – Latin American Art Experience  
### Final Project – Stage 2: Code Implementation & Testing  
### Southern Utah University – CS 2450  
---

## 📌 Overview  
This project implements an interactive art‑exploration system called **Mestizaje**, designed to showcase artworks from Latin American countries.  
Users swipe through random artworks, “like” the ones they prefer, and see which country becomes their favorite at the end.  

The system follows the **MVC architecture**, uses **Factory Method** as its main design pattern, loads data dynamically from JSON, and includes a fully functional **Tkinter GUI** with animations.

---

## 🧱 System Architecture

### **1. Models (src/models/)**
- **Country** – stores metadata, list of artists, and keeps track of a country score.
- **Artist** – reference to the country and container for artworks.
- **Artwork** – stores artwork path and metadata.

### **2. Factories (src/models/factories.py)**
Implements the **Factory Method** pattern for:
- Creating Country objects  
- Creating Artist objects  
- Creating Artwork objects  

This ensures consistent object construction and clean separation from the JSON structure.

---

## 🎮 Controller Layer  
The controller coordinates:
- Random artwork selection  
- Session progress tracking (e.g., 1/40)  
- Storing likes  
- Returning final favorite countries  

Located in: `src/controller/swipe_manager.py`

---

## 🎨 View Layer  
Written with **Tkinter**, including:
- Fade‑in animations  
- Swipe left/right animations  
- “Show Info” overlay  
- Settings screen to choose artwork count  

Located in: `src/view/tk_view.py`

---

## 📁 Loader  
### `DatasetLoader`
Loads the JSON database and converts each entry into Country, Artist, and Artwork objects using the factory pattern.

JSON lives in:
```
src/data/dataset.json
```

---

## 🧪 Testing  
Inside `/tests/`:

### **1. Unit Tests**
- Test model initialization  
- Test factories  
- Test dataset loader  

### **2. Integration Tests**
- Ensures real file paths exist  
- Ensures countries/artists/artworks link together properly  

Run tests:
```
python -m unittest discover tests
```

---

## ▶️ Running the Program  
From the project root directory:

```
python -m src.main
```

---

## 📄 Deliverables Included
- Full source code folder  
- README.md (this file)  
- Test results (screenshots or terminal output)  
- Stage 2 Implementation PDF  

---

## ✨ Notes  
This project was built with modularity, clarity, and maintainability in mind.  
Key OOP principles applied:
- Encapsulation  
- Composition  
- Separation of concerns  
- Factory Method pattern  

The GUI adds an optional interactive layer that aligns with the project’s creative purpose.

---

## 👨‍🏫 Instructor Notes  
This README summarizes:
- Architecture  
- System components  
- Design pattern usage  
- Testing implementation  

Fulfills Stage 2 requirements.

