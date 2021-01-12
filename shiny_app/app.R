library(shiny)


champion_info <- read.table("data/champion_list.csv", header = TRUE, row.names = 1, sep = ",", quote = "\"", check.names = FALSE)
champions <- champion_info[,"names"]; names(champions) <- champions
names(champions) <- replace(names(champions), names(champions) == "MonkeyKing", "Wukong")
champions <- champions[order(names(champions))]
# Define UI for app that draws a histogram ----
ui <- fluidPage(theme = "bootstrap.css",
  titlePanel(title = "Shiny counters", windowTitle = "Shiny counters"),
  selectInput(inputId = "selectChampion", label = "Select Champion", 
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