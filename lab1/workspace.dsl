workspace "Приложение для управления проектами"{
    
    !identifiers hierarchical
    
    model {
        user = person "Пользователь"
        app = softwareSystem "Разработ очка" {
            description "Приложение для управления проектами"
            
            user_service = container "Сервис пользователей" {
                description "Реализует взаимодействие пользователя с проектами"
                technology "python3, jwt"
            }
            project_service = container "Сервис проектов" {
                description "Реализует функционал работы проекта"
                technology "python3"
            }
            board_service = container "Сервис тасок" {
                description "Реализует функционал работы доски"
                technology "python3"
            }
            
            group "Слой хранения" {
                user_db = container "База данных пользователей" {
                    description "Хранит данные о пользователях"
                    technology "postgresql"
                    tags "database"
                }
                project_db = container "База данных проектов" {
                    description "Хранит данные о проектах"
                    technology "postgresql"                    
                    tags "database"
                }
                task_db = container "База данных тасок" {
                    description "Хранит информацию о тасках"
                    technology "postgresql"
                    tags "database"
                }
            }
        }
        user -> app "Получает информацию о проекте"
        user -> app.user_service "Получает информацию об исполнителях"
        user -> app.project_service "Администрирует проекты"
        user -> app.board_service "Двигает карточки внутри проекта"
        app.user_service -> app.user_db "Хранит информацию о пользователях и их задачах"
        app.project_service -> app.project_db "Хранит информацию о проектах"
        app.project_service -> app.user_service "Получает информацию о пользователях внутри проекта"
        app.project_service -> app.board_service "Получает информацию о задачах внутри проекта"
        app.board_service -> app.user_service "Получает информацию об исполнителе"
        app.board_service -> app.task_db "Хранит информацию о тасках"
        app.task_db -> app.project_db "Привязка задач к проектам"
        
    }
    
    views {
        themes default

        properties { 
            structurizr.tooltips true
        }
        
        systemContext app "Context" {
            include *
            autoLayout 
        }

        container app "Container" {
            include *
            autoLayout
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
        
        dynamic app "CreateUser" "Создание нового пользователя" {
            autolayout
            user -> app.user_service "Создать нового пользователя (POST /user)"
            app.user_service -> app.user_db "Сохранить данные о пользователе"
        }
        
        dynamic app "CreateTask" "Создание новой таски" {
            autolayout
            user -> app.board_service "Создать новую задачу (POST /task)"
            app.board_service -> app.project_service "Обновить проект (POST /project/task)"
            app.project_service -> app.project_db "Обновить данные о проекте"
            app.board_service -> app.task_db "Сохранить данные о таске"
        }
        
        dynamic app "CreateProject" "Создание проекта" {
            autolayout
            user -> app.project_service "Создать новый проект (POST /project)"
            app.project_service -> app.project_db "Сохранить данные о проекте"
        }
        
        dynamic app "FindUserByLogin" "Поиск пользователя по логину" {
            autolayout
            user -> app.user_service "Найти пользователя (GET /user/search/login)"
            app.user_service -> app.user_db "Найти данные о пользователе"
        }
        
        dynamic app "FindUserByName" "Поиск пользователя по маске имени и фамилии" {
            autolayout
            user -> app.user_service "Найти пользователя (GET /user/search/name)"
            app.user_service -> app.user_db "Найти данные о пользователе"
        }
        
        dynamic app "FindProjectByName" "Поиск проекта по названию" {
            autolayout
            user -> app.project_service "Найти пользователя (GET /project/search/project_name)"
            app.project_service -> app.project_db "Найти проект по названию"
        }
        
        dynamic app "FindAllProjects" "Поиск всех проектов пользователя" {
            autolayout
            user -> app.project_service "Найти все проекты (POST /project/search/name)"
            app.project_service -> app.user_service "Найти пользователя (GET /user/search/login)"
            app.user_service -> app.user_db "Получить данные о пользователе"
            app.project_service -> app.project_db "Получить данные о проектах (GET /project/search/project_name)"
        }
        
        dynamic app "AddUserToProject" "Добавление пользователя в проект" {
            autolayout
            user -> app.project_service "Добавить пользователя в проект (POST /project/add)"
            app.project_service -> app.user_service "Найти пользователя (GET /user/search/login)"
            app.user_service -> app.user_db "Получить данные о пользователе"
            app.project_service -> app.project_db "Обновить данные о проекте"
        }
        
        dynamic app "AddAssigneeToTask" "Добавление исполнителя в таску" {
            autolayout
            user -> app.board_service "Добавление исполнителя в таску (POST /task/add)"
            app.board_service -> app.user_service "Поиск информации об исполнителе (GET /user/search/login)"
            app.user_service -> app.user_db "Получение информации об исполнителе"
            app.board_service -> app.task_db "Обновление информации о таске"
        }
        
        dynamic app "FindTaskByID" "Поиск задачи по коду (ID)" {
            autolayout 
            user -> app.board_service "Найти таску (GET /task/search/id)"
            app.board_service -> app.task_db "Получить данные о таске"
        }
        
        dynamic app "FindAllTasksInProject" "Получение всех задач в проекте" {
            autolayout 
            user -> app.project_service "Найти все таски в проекте (GET /project/search/tasks)"
            app.project_service -> app.project_db "Получение информации о проекте"
            app.project_service -> app.board_service "Поиск задач (GET /task/search/id)"
            app.board_service -> app.task_db "Получение информации о таске"
        }
        
        dynamic app "UpdateTaskStatus" "Обновление статуса таски" {
            autolayout
            user -> app.board_service "Обновление статуса таски (Post /task/update)"
            app.board_service -> app.task_db "Обновить информацию о таске"
        }
    }
   
}