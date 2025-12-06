# Mestizaje – Latin American Art Experience
Valeria Poveda and Rebekah Jensen

**Project Overview**

Mestizaje is an interactive art-exploration application that displays randomized artworks from Latin American countries. Users swipe to indicate preference, and the system determines a final preferred country based on cumulative selections.

The project implements the Model–View–Controller (MVC) architectural pattern, applies the Factory Method design pattern, loads data dynamically from a JSON dataset, and provides a functional graphical interface developed with Tkinter. The system emphasizes modularity, maintainability, and clear separation of responsibilities.

**System Architecture**

Models (src/models/)
The data layer is composed of three primary classes:

- Country  
  - Stores metadata about each country  
  - Maintains a cumulative score used to determine preference  
  - Contains a list of associated artists  

- Artist  
  - Associated with a specific country  
  - Contains a collection of artworks  

- Artwork  
  - Stores metadata and an image file path  

Factory Layer (src/models/factories.py)
- The application uses the Factory Method pattern to construct Country, Artist, and Artwork objects.  This design choice enforces consistent object creation and ensures a clear separation between the JSON structure and internal model representation.

**Controller Layer (src/controller/swipe_manager.py)**

The controller manages the core application logic, including:

- Selecting randomized artworks  
- Tracking user progress throughout the session  
- Recording positive swipes  
- Determining the final preferred country  

The controller mediates communication between the model layer and the graphical interface.

**View Layer (src/view/tk_view.py)**

The graphical interface is implemented using Tkinter. It includes:

- Visual transitions such as fade-in and swipe animations  
- An informational overlay displaying artwork metadata  
- Keyboard and button-based interaction  
- A settings interface allowing users to select the number of artworks to view  

The view remains independent from business logic in accordance with MVC principles.

**Dataset Loader (src/loader/dataset_loader.py)**

The DatasetLoader is responsible for:

- Reading and parsing the JSON dataset located in src/data/dataset.json  
- Constructing model objects using the factory classes  
- Validating relationships among countries, artists, and artworks  

This component centralizes all data loading to maintain consistency across the application.

**Testing**

All tests are located in the tests/ directory.

Unit Tests
- Unit tests verify:

  - Correct initialization of model classes  
  - Expected behavior of factory methods  
  - Proper handling of JSON data by the DatasetLoader  

Integration Tests
- Integration tests validate:

  - Correctness of artwork file paths  
  - Proper relationships between Country, Artist, and Artwork  
  - Interaction between loader, controller, and model components
 
Tests can be run using: python -m unittest discover tests


**Running the Application**

From the project root directory, the program can be executed with: python src/main.py


**Software Engineering Principles Applied**
- Encapsulation  
- Composition  
- Separation of concerns  
- Use of the Factory Method design pattern  
- Modular and extensible architecture appropriate for future development

