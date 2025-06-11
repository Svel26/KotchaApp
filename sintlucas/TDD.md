# Technical Design Document: Albert Heijn Collectibles Mobile Website

### 1. Introduction
[cite_start]This document outlines the technical design for a mobile website that allows users to collect virtual Albert Heijn characters.  [cite_start]The website will feature an interactive 3D environment representing different sections of an Albert Heijn store.  [cite_start]Users can discover characters by navigating these 3D snippets, and physically collect them by scanning NFC tags embedded in 3D-printed figures obtained in-store.  [cite_start]The platform will provide clues for uncollected characters and food waste-related information for collected ones. 

### 2. Goals
* [cite_start]Create an engaging and interactive mobile website using 3D elements powered by Three.js. 
* [cite_start]Allow users to virtually explore different store sections to discover collectible characters. 
* [cite_start]Implement a system where uncollected characters are visually represented as blacked-out with a question mark. 
* [cite_start]Provide a riddle/hint for uncollected characters upon clicking their placeholder. 
* [cite_start]Display product information with a food waste focus for collected characters upon clicking their 3D representation. 
* [cite_start]Enable character collection through NFC scanning. 
* Utilize Vue.js for the frontend framework to manage the application state and UI components.
* [cite_start]Maintain the visual style and branding of Albert Heijn. 
* Store application data in a database.

### 3. Target Audience
[cite_start]Customers of Albert Heijn, particularly children interested in collecting the in-store promotional items. 

### 4. Technical Stack
* **Frontend Framework:** Vue.js
* **3D Graphics Library:** Three.js
* **NFC Interaction:** Web NFC API
* **State Management (optional):** Vuex
* **Styling:** CSS
* [cite_start]**Data Storage:** Database 

### 5. System Architecture
The application will primarily be a frontend-heavy single-page application (SPA) built with Vue.js and Three.js.

* [cite_start]**3D Environment:** Three.js will be used to render interactive 3D snippets of different store sections (e.g., bakery, produce, dairy).  [cite_start]These will be provided as 3D models by the MV team. 
* [cite_start]**Character Representation:** Each collectible character will have a 3D model.  [cite_start]The application will manage the state of each character (collected or uncollected). 
* [cite_start]**UI Components:** Vue.js components will be responsible for rendering the store navigation, character displays, information modals, and any other interactive elements. 
* **Data Management:** A Database will store information about the collectibles, including:
    * Character ID
    * Name
    * Store Section Association
    * 3D Model Path
    * Riddle/Hint (for uncollected)
    * Product Information
    * Food Waste Tip (for collected)
    * [cite_start]NFC Tag ID (linking the physical NFC tag to the digital character) 
* **NFC Handling:** The Web NFC API will be used to read the unique ID from the NFC tags embedded in the physical collectibles. [cite_start]This ID will be matched against the data in the database to mark the corresponding character as collected. 

### 6. Detailed Design

#### 6.1. 3D Store Navigation
[cite_start]The main view will present a way to swipe horizontally through different 3D snippets representing store areas.  [cite_start]Each snippet will visually suggest the type of collectibles that might be found there (e.g., bread in the bakery section).  [cite_start]Performance on mobile will be a key consideration for the complexity and optimization of these 3D scenes. 

#### 6.2. Character Display
[cite_start]Within each 3D store section, the collectible characters associated with that section will be displayed. 
* [cite_start]**Uncollected Characters:** Will be rendered as a blacked-out silhouette with a question mark overlay. 
* [cite_start]**Collected Characters:** Will be rendered in full color and detail based on the 3D models provided. 
[cite_start]Clicking on a character (or its placeholder) will trigger a modal or overlay. 

#### 6.3. Information Modals/Overlays
* [cite_start]**Uncollected Character:** The modal will display the riddle/hint associated with that character, providing a clue about the Albert Heijn product needed to "collect" it (via the physical NFC figure). 
* [cite_start]**Collected Character:** The modal will display information about the corresponding product and a food waste-related tip. 

#### 6.4. NFC Scanning
[cite_start]The application will need a clear call-to-action (e.g., a button or prompt) to initiate the NFC scanning process.  [cite_start]Upon scanning an NFC tag, the application will read the unique ID.  [cite_start]This ID will be compared against the NFC Tag ID stored in the database.  [cite_start]If a match is found and the character is not yet collected, the character's state will be updated to "collected," and its visual representation in the 3D scene will change.  [cite_start]The collected state should be persistent. 

#### 6.5. State Management (Vuex)
Vuex can help manage the application's state (e.g., the list of collectibles, the collected status of each, the currently displayed store section). [cite_start]This will make the application more organized and maintainable as it grows.  [cite_start]However this is not the plan for now. 

#### 6.6. Albert Heijn Styling
[cite_start]The color palette, typography, and overall visual language of the website should closely resemble Albert Heijn's branding.  [cite_start]The MV team will play a crucial role in providing assets and guidance on this. 

### 7. User Interface (UI) Considerations
* [cite_start]**Mobile-First Design:** The website must be designed and developed with mobile devices as the primary target. 
* [cite_start]**Intuitive Navigation:** Swiping between store sections should be smooth and responsive. 
* [cite_start]**Clear Visual Cues:** Collected and uncollected characters should be easily distinguishable. 
* [cite_start]**Accessibility:** Consider basic accessibility guidelines to ensure usability for a wider audience. 
* [cite_start]**NFC Interaction Guidance:** Provide clear instructions to the user on how to scan the NFC tags. 

### 8. Development Process & Team Collaboration
* [cite_start]**Mediavormgeving Team:** Responsible for creating and optimizing the 3D models of the store snippets and collectible characters, as well as providing branding assets. 
* [cite_start]**Software Development Team:** Responsible for the frontend development using Vue.js and Three.js, implementing the NFC functionality, managing the data, and ensuring mobile performance. 
[cite_start]Close collaboration between both teams will be essential to ensure the 3D assets are integrated seamlessly into the web application and that the visual style aligns with Albert Heijn's branding. 

### 9. Potential Challenges & Considerations
* [cite_start]**Mobile Performance:** Rendering complex 3D scenes on mobile devices can be performance-intensive.  [cite_start]Optimization of 3D models, efficient Three.js usage, and careful consideration of rendering techniques will be crucial. 
* [cite_start]**Web NFC API Support:** The Web NFC API might not be universally supported across all mobile browsers.  [cite_start]A fallback mechanism or clear communication about browser compatibility might be necessary. 
* [cite_start]**NFC Tag Reading Reliability:** Ensure robust error handling and clear feedback to the user during the NFC scanning process. 
* [cite_start]**Maintaining Albert Heijn's Style:** Close collaboration with the design team is needed to accurately replicate their visual identity. 
* [cite_start]**Scalability (Beyond School Project):** If this project were to scale beyond a school exercise, a proper backend database and API would be necessary for managing data and user accounts. 

### 10. Future Enhancements (Beyond Initial Scope)
* [cite_start]Integration with a user account system (if Albert Heijn API access were available or a custom system was built). 
* [cite_start]Gamification elements (e.g., badges, leaderboards). 
* Social sharing features.
* Small minigame(s)

### 11. MoSCoW

| Must Have | Should Have | Could Have | Wont Have |
| :--- | :--- | :--- | :--- |
| Swipeable 3D Store Sections | Vue.js Framework Implementation | Vuex for State Management | |
| Collectible Character Display (3D) | Three.js for 3D Rendering | Smoother 3D Transitions/Animations | Trading or Social Features |
| Uncollected Character Placeholder | Basic Albert Heijn Styling | NFC Scanning Instructions/Feedback | Augmented Reality (AR) Features |
| Riddle/Hint for Uncollected Characters | | More Advanced 3D Interactions | |
| Collected Character Information | | Integration with Albert Heijn Account via API | |
| NFC Scanning for Collection | | User Accounts | |
| Updating Collection Status | | | |
| Persistence of Collected Data (Local Storage) | | | |
| Database for data storage | | | |
[cite_start][cite: 55]
