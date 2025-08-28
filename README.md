## ROAM National Parks API
[ROAM-NationalParks Repo](https://github.com/sigreipel/ROAM-NationalParks)

ROAM-NationalParks is a full-stack web application that allows users to explore and discover U.S. National Parks through an interactive interface. The platform pulls real-time data from the National Park Service API and supports searching by park name or filtering by activity. With a custom authentication system, users can log in to personalize their experience. The project is built using React (frontend) and Flask (backend), with CI/CD managed through Azure DevOps.

<ins>Features:</ins>

- Search by Park Name or Activity
- Browse parks by name or filter them by supported activities like hiking, stargazing, or camping.
- View detailed information including descriptions, activities, location data, and park images.
- Uses the National Park Service API to retrieve accurate, up-to-date real-time park information.
- Custom login system allows users to securely log in and access personalized features.

<ins>User Personalization (Future Integration)</ins>
- Save favorite parks or build travel itineraries
- User dashboard with visited and saved parks
- Block or hide parks not of interest

<ins>Backend</ins>

- Built with Flask to handle API requests and data filtering
- Structured endpoints for search and activity-based queries
- Authentication logic integrated into the backend

<ins>TechStack:</ins>

- Frontend: React, Tailwind CSS or Material UI
- Backend: Flask (Python)
- Authentication: Custom login system using Flask
- API Integration: National Park Service API
- Deployment: Azure DevOps Pipelines

<ins>Future Improvements</ins>

- Expand login system to support registration and profile management
- Add support for saving and sharing park itineraries
- Integrate weather and alert data for real-time planning
- Enhance search and suggestions with machine learning
- Expand Azure DevOps pipeline with automated testing and environment configs
