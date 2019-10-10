#2.1Load bcw_processed.Rda
bcw2<-load("bcw_processed.Rda")

#Select first nine variables
bcw3 <- bcw1[,1:9]
#For reproducible result
set.seed(2835)

#2.2Cluster the data into 2 clusters
nclust = 2
bcw3 <- bcw1[,1:9]
(kmeans.result <- kmeans(bcw3,nclust))

#Plot
plot(bcw1[,c("Clump.Thickness","Uniformity.of.Cell.Size")])
title(paste("k= ",nclust,sep=""))

#2.3Color the points according to the Class column
bcw3 <- bcw[,1:9]
nclust = 2
(kmeans.result <- kmeans(bcw3,nclust))
plot(bcw1[,c("Clump.Thickness","Uniformity.of.Cell.Size")],
     col = bcw1$Class)
title(paste("k= ",nclust,sep=""))

#2.5 Cluster more than 2
#when cluste =3
bcw3 <- bcw[,1:9]
nclust = 3
(kmeans.result <- kmeans(bcw3,nclust))
plot(bcw1[,c("Clump.Thickness","Uniformity.of.Cell.Size")],
     col = kmeans.result$cluster)
title(paste("k= ",nclust,sep=""))
points(kmeans.result$centers[,c("Clump.Thickness","Uniformity.of.Cell.Size")],
       col=1:nclust, pch = 4, cex = 4)

#when nclust = 4
bcw3 <- bcw[,1:9]
nclust = 4
(kmeans.result <- kmeans(bcw3,nclust))
plot(bcw1[,c("Clump.Thickness","Uniformity.of.Cell.Size")],
     col = kmeans.result$cluster)
title(paste("k= ",nclust,sep=""))
points(kmeans.result$centers[,c("Clump.Thickness","Uniformity.of.Cell.Size")],
       col=1:nclust, pch = 2, cex = 4)

#when nclust=5
bcw3 <- bcw[,1:9]
nclust = 5
(kmeans.result <- kmeans(bcw3,nclust))
plot(bcw1[,c("Clump.Thickness","Uniformity.of.Cell.Size")],
     col = kmeans.result$cluster)
title(paste("k= ",nclust,sep=""))
points(kmeans.result$centers[,c("Clump.Thickness","Uniformity.of.Cell.Size")],
       col=1:nclust, pch = 2, cex = 4)

#2.7hierarchical clustering with hclust function
hc <- hclust(dist(bcw1))
#plot the obtained dendrogram
plot(hc,hang=-1)

#Cluster the dendrogram into nclust clusters
#when n =2
#hierarchical clustering with hclust function
hc <- hclust(dist(bcw1))
#plot the obtained dendrogram
plot(hc,hang=-1)

#Cluster the dendrogram into nclust clusters
#when n =2
nclust = 2
rect.hclust(hc,k=nclust)
groups <- cutree(hc,k=nclust)

#when n=3
nclust = 3
rect.hclust(hc,k=nclust)
groups <- cutree(hc,k=nclust)

#when n =4
nclust = 4
rect.hclust(hc,k=nclust)
groups <- cutree(hc,k=nclust)

#when n =5
nclust = 5
rect.hclust(hc,k=nclust)
groups <- cutree(hc,k=nclust)

#2.9 Cluster with methods
#single
hc <- hclust(dist(bcw1),method="single")
plot(hc,hang=-1)

#complete
hc <- hclust(dist(bcw1),method="complete")
plot(hc,hang=-1)

#average
hc <- hclust(dist(bcw1),method="average")
plot(hc,hang=-1)

#save file
save(bcw1.file="./code/myClustering.r")