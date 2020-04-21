
(
    vuepress build &&
    cd .vuepress/dist &&
    chmod -R 777 ../dist &&
    http-server -p 5000
)
