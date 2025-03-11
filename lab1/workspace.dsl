workspace "Приложение для управления проектами"{
    
    !identifiers hierarchical
    
    model {
        user = person "Пользователь"
        app = softwareSystem "Разработ очка" {
            description "Приложение для управления проектами"
            
            user_service = container "Сервис пользователей" {
                description "Реализует взаимодействие пользователя с проектами"
            }
            project_service = container "Сервис проектов" {
                description "Реализует функционал работы проекта"
            }
            board_service = container "Сервис тасок" {
                description "Реализует функционал работы доски"
            }
            
            group "Слой хранения" {
                user_db = container "База данных пользователей" {
                    description "Хранит данные о пользователях"
                    tags "database"
                }
                project_db = container "База данных проектов" {
                    description "Хранит данные о проектах"
                    tags "database"
                }
                task_db = container "База данных тасок" {
                    description "Хранит информацию о тасках"
                    tags "database"
                }
            }
        }
        user -> app "Получает информацию о проекте"
        user -> app.user_service "Получает информацию о задачах"
        user -> app.project_service "Администрирует проекты"
        user -> app.board_service "Двигает карточки внутри проекта"
        app.user_service -> app.user_db "Хранит информацию о пользователях и их задачах"
        app.project_service -> app.project_db "Хранит информацию о проектах"
        app.project_service -> app.user_service "Получает информацию о пользователях"
        app.user_service -> app.project_service "Получает информацию о проекте"
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
            user -> app.board_service "Создать новую задачу (Post /task)"
            app.board_service -> app.task_db "Сохранить данные о таске"
        }
        
        dynamic app "CreateProject" "Создание проекта" {
            autolayout
            user -> app.project_service "Создать новый проект (Post /project)"
            app.project_service -> app.project_db "Сохранить данные о проекте"
        }
        
        dynamic app "FindUserByLogin" "Поиск пользователя по логину" {
            autolayout
            user -> app.user_service "Найти пользователя (Get /user/search/login)"
            app.user_service -> app.user_db "Найти данные о пользователе"
        }
        
        dynamic app "FindUserByName" "Поиск пользователя по маске имени и фамилии" {
            autolayout
            user -> app.user_service "Найти пользователя (Get /user/search/name)"
            app.user_service -> app.user_db "Найти данные о пользователе"
        }
    }
   
}
