#Para que este codigo funcione, colocar el directorio de trabajo en la carpeta
#data del proyecto
library(rjson)

data <- fromJSON(file = 'matches.json')
a = data[[1]]
champion_codes = list()


getChampions <- function(match){
  return(c(match$blue$picks, match$red$picks))
}

picks <- lapply(data, getChampions)

champions_played <- unique(unlist(picks))
champions_played <- sapply(champions_played, as.character)

results <- matrix(0, nrow = length(champions_played) + 1,
                  ncol = length(champions_played) + 1)
colnames(results) <- c(champions_played, "totalWins")
rownames(results) <- c(champions_played, "totalLoses")

x <- c("blue", "red")
for(match in data){
  winners <- c(unlist(lapply(get(match$win, match)$picks, as.character)), "totalLoses")
  losers <- c(unlist(lapply(get(x[x != match$win], match)$picks, as.character)), "totalWins")
  results[winners, losers] <- results[winners, losers] + 1
}
rm(winners, losers, x)

write.csv(results, "winrate_matrix.csv")

#Codigo para cargar los datos de manera correcta
#pr <- as.matrix(read.table("winrate_matrix.csv", header = TRUE, row.names = 1, sep = ",", quote = "\"", check.names = FALSE))
