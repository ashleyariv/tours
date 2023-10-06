# Models

 - Doctor 
    - id        (integer, primary key)
    - name      (string, not null)
    - specialty (string, not null)
 - Appointment
    - id         (integer, primary key)
    - day        (string, not null)
    - doctor_id  (integer, not null)
    - patient_id (integer, not null)
 - Patient
    - id   (primary key)
    - name (string, not null)
# Validation

  - Doctor
    - names must start with 'Dr.'
  - Appointment
    - day must be between Monday and Friday
    
# Routes

  - GET /doctors
  - GET /doctors/<int:id>
  - POST /doctors
  - GET /patients/<int:id>
  - PATCH /patients/<int:id>
  - POST /appointments
  - DELETE /appointments/<int:id>
    

# Response Formats

  - GET /doctors
  ```json
  [
      {
          id
          name
          specialty
      }
  ]
  ```
  - GET /doctors/<int:id>
  ```json
  [
      {
          id
          name
          specialty
          appointments: [
            {
                id
                day
                patient: {
                    id
                    name
                }
            }
          ]
      }
  ]
  ```
  - GET /patients/<int:id>
    ```json
      {
          id
          name
          doctors: [
            {
                id
                name
                specialty
            }
          ]
      }
  ```
  - POST /doctors
  ```json
      {
          id
          name
          specialty
      }
  ```
  - PATCH /patients/<int:id>
  ```json
      {
          id
          name
      }
  ```
  - POST /appointments
    ```json
      {
        id
        doctor: {
            id
            name
            specialty
        }
        patient: {
            id
            name
        }
      }
  ```