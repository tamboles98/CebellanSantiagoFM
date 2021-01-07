library(shiny)


champion_info <- read.table("data/champion_list.csv", header = TRUE, row.names = 1, sep = ",", quote = "\"", check.names = FALSE)
champions <- champion_info[,"names"]; champions <- sort(champions); names(champions) <- champions
# Define UI for app that draws a histogram ----
ui <- fluidPage(theme = "bootstrap.css",
  titlePanel(title = "Shiny counters", windowTitle = "Shiny counters"),
  selectInput("selectChampion", h3("Select Champion"), 
              choices = champions),
  imageOutput("my_ui")
)

# Define server logic required to draw a histogram ----
server <- function(input, output) {
  output$my_ui <- renderImage({
    filename <- normalizePath(file.path('./www/champion_squares',
                                        paste(input$selectChampion, '.png', sep='')))
    list(src = filename, width = 80)}, deleteFile = FALSE)
}

shinyApp(ui = ui, server = server)