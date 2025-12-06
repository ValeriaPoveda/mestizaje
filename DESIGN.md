# Design

**Overview**

Mestizaje is a Tkinter-based swipe application that showcases Latin American art. It loosely follows the Model–View–Controller (MVC) structure:

- Models (src/models/): Country, Artist, and Artwork store metadata and relationships; Session and Swipe track user choices; factories centralize construction.  
- Controller (src/controller/swipe_manager.py): Coordinates sessions, flattens and samples artworks, advances swipes, and reports results and counters.  
- Loader (src/loader/dataset_loader.py): Reads data/dataset.json, creates models through factories, and resolves artwork files on disk.  
- View (src/view/tk_view.py): Tkinter GUI with fade and slide animations, glass-like styling, fullscreen launch, and controls for skip, info, and like.

**Key Classes**

- Country, Artist, Artwork: Data holders linking countries, artists, and artwork paths.  
- Session: Records swipes and computes top-liked countries.  
- SwipeManager: Manages artwork ordering, current index, swipes, and final results.  
- DatasetLoader: Validates the dataset, builds model objects, and flexibly resolves image paths.  
- TkView: Implements all screens (settings, start, swipe, results) and animations while calling controller APIs.

**Design Decisions**

- The factory pattern keeps the loader decoupled from model constructors.  
- Flexible path resolution searches declared paths plus `artworks/batch1` and `artworks/batch2`, with extension and digit-only filename fallbacks, allowing reorganized assets to load without modifying the JSON dataset.  
- Session isolation provided by `start_session` enables replay; like-counting resides in Session, not the controller.  
- Clear separation between UI and logic prevents styling updates from affecting core behavior.  
- Pillow-based animations handle fade and slide transitions within Tkinter.

#**Notable Behaviors**

- “Show Info” uses a blue accent button while keeping the control layout unchanged.  
- The image loader falls back to a gray placeholder when files cannot be resolved.  
- Tests cover dataset structure, path existence (batch-aware), loader and model wiring, and SwipeManager behavior.

**Reflections**

- Layered fallbacks for assets (names, extensions, batch roots) increased resilience to filesystem changes.  
- A thin view layer kept UI restyling low-risk.  
- Simple factories and structured loader logic supported dataset evolution without affecting the UI or controller layers.

**Challenges**

- Inconsistent or missing assets across batches required careful path resolution to avoid runtime errors.  
- Achieving a modern or glass-like visual feel in Tkinter while maintaining stable layout required iterative adjustments to sizing and padding.

**Future Improvements**

- Display a UI message when zero artworks resolve (currently logged as a controller error).  
- Add a headless or command-line mode for environments without Tk.  
- Cache resolved paths to reduce filesystem lookups on large datasets.  
- Add targeted tests for batch path resolution and UI smoke or snapshot tests.
