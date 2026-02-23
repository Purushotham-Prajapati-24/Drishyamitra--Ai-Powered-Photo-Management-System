# Drishyamitra: Product Requirement Document (PRD) & Customer Journey Map

## 1. Project Overview
**Drishyamitra** is an AI-powered photo management system designed to automate the organization, search, and sharing of digital memories. By leveraging deep learning-based facial recognition and natural language processing, it transforms a static photo gallery into an intelligent, conversational ecosystem.

---

## 2. Product Requirement Document (PRD)

### 2.1 Target Audience
* **Individual Users:** Families looking to organize years of unsorted digital photos.
* **Event Organizers:** Photographers needing to sort and deliver photos to specific attendees automatically.
* **Corporate Teams:** Marketing departments managing large libraries of brand and event assets.

### 2.2 Functional Requirements
* **AI Face Recognition & Clustering:** * Automatic detection using RetinaFace/MTCNN.
    * Generation of 512-d embeddings for high-accuracy matching.
    * Automatic grouping of images into person-specific "Smart Folders."
* **Conversational AI Assistant:**
    * Natural language interface to query the gallery (e.g., "Find photos of Arjun from the trip").
    * Ability to trigger actions (sharing/deleting) via chat commands.
* **Automated Delivery System:**
    * Integration with **Gmail** for professional/official photo sharing.
    * Integration with **WhatsApp** for instant social sharing.
* **Security & User Management:**
    * JWT-based authentication for secure session management.
    * Bcrypt hashing for password protection.
    * Private database instances for user-specific photo metadata.

### 2.3 Non-Functional Requirements
* **Performance:** Background processing for heavy image analysis to prevent UI lag.
* **Scalability:** Modular backend to support future cloud synchronization.
* **Usability:** Mobile-responsive dashboard built with modern UI standards.

---

## 3. Technology Stack

### Frontend
* **Framework:** React.js
* **Styling:** Tailwind CSS & Framer Motion (for animations)
* **Icons:** Lucide React
* **State/API:** Axios & Context API

### Backend
* **Language/Framework:** Python / Flask
* **Database:** SQLAlchemy (PostgreSQL/SQLite)
* **Async Tasks:** Celery with Redis (for image processing)
* **Security:** Flask-JWT-Extended & Bcrypt

### AI & Integrations
* **Computer Vision:** DeepFace (Facenet512, RetinaFace, MTCNN)
* **LLM (Chatbot):** Groq API (Llama 3.3 70B / Mixtral)
* **Communication:** SMTP (Gmail) & WhatsApp Web API

---

## 4. Customer Journey Mapping (CJM)

| Stage | **Discovery & Setup** | **Data Ingestion** | **AI Organization** | **Search & Retrieval** | **Action & Sharing** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **User Action** | Registers account and logs into the dashboard. | Uploads a bulk folder of wedding or vacation photos. | Views the "Smart Folders" section where faces are grouped. | Asks the chatbot: "Find photos of Sarah." | Clicks "Share to WhatsApp" or "Email to Client." |
| **System Process** | Flask authenticates via JWT; React loads user profile. | Celery picks up images; DeepFace extracts embeddings. | Clustering algorithm assigns images to IDs; metadata updated. | Groq API parses intent; Backend queries the database. | Triggers SMTP for Email or Webhook for WhatsApp. |
| **User Emotion** | Neutral / Curious | Anxious (Will it handle 500 photos?) | **Delighted** (The AI recognized everyone!) | **Empowered** (No more manual scrolling.) | **Satisfied** (Tasks finished in seconds.) |
| **Pain Points** | Manual data entry for profile setup. | Processing time for very large batches. | Occasional mis-grouping in low-light photos. | Vague queries leading to broad results. | Re-authenticating external APIs (WhatsApp). |

---

## 5. Success Metrics
* **Accuracy Rate:** Percentage of correctly identified faces (>95% target).
* **Processing Speed:** Average time taken to index 100 images.
* **Engagement:** Frequency of chatbot usage vs. manual folder browsing.
* **Delivery Success:** Rate of successful WhatsApp/Email transmissions.