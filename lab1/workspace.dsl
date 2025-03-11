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
            
            group "Слой хранения" {
                user_db = container "База данных пользователей" {
                    description "Хранит данные о пользователях"
                    tags "database"
                }
                project_db = container "База данных проектов" {
                    description "Хранит данные о проектах"
                    tags "database"
                }
            }
        }
        user -> app "Получает информацию о проекте"
        user -> app.user_service "Получает информацию о задачах"
        user -> app.project_service "Администрирует проекты"
        app.user_service -> app.user_db "Хранит информацию о пользователях и их задачах"
        app.project_service -> app.project_db "Хранит информацию о проектах"
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
    }
   
}