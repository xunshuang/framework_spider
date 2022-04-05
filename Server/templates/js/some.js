// 创建三级目录
function showDetails(t1, t2, t3) {
    var machineType1 = t1
    var machineType2 = t2
    var machineType3 = t3
    if (machineType1 && !machineType2) {
        levelOne = machineType1
        levelTwo = ""
        levelThree = ""
        // var level1 = document.getElementById('level1') //目录第一级
        var level2 = document.getElementById('level2') //目录第二级
        var level3 = document.getElementById('level3') //目录第三级
        machineDict.forEach(function (item, index) {
            if (item["levelName"] === levelOne) {
                while (1) {
                    try {
                        level2.removeChild(level2.childNodes[0])
                    } catch (e) {
                        break
                    }
                }
                while (1) {
                    try {
                        level3.removeChild(level3.childNodes[0])
                    } catch (e) {
                        break
                    }
                }
                if (item.child != false) {
                    item['child'].forEach(function (item, index) {
                        var newNode = document.createElement("button")
                        newNode.innerHTML = item["levelName"]
                        var _ = item["levelName"]
                        newNode.onclick = function () {
                            showDetails(t1 = t1, t2 = _)
                            var nodes = document.getElementById('level2').childNodes
                            nodes.forEach(function (item, index) {
                                try {
                                    item.style.backgroundColor = "white"
                                    item.style.color = "grey"
                                } catch (e) {
                                    //TODO handle the exception
                                }

                            })
                            newNode.style.backgroundColor = "#fb5e33"
                            newNode.style.color = "white"
                        }
                        newNode.setAttribute("class", "machineClass")

                        level2.appendChild(newNode)
                    })
                } else {
                    sendMsg(t1 = levelOne)
                }

            }
        })

        document.getElementById('level2').removeAttribute("hidden")

    }
    if (machineType1 && machineType2 && !machineType3) {
        levelTwo = machineType2
        levelThree = ""
        var level3 = document.getElementById('level3')
        machineDict.forEach(function (item, index) {
            if (item.levelName === levelOne) {
                item.child.forEach(function (item, index) {

                    if (item["levelName"] === levelTwo) {
                        while (1) {
                            try {
                                level3.removeChild(level3.childNodes[0])
                            } catch (e) {
                                break
                            }
                        }
                        ;
                        if (item.child != false) {
                            item['child'].forEach(function (item, index) {
                                var newNode = document.createElement("button")
                                newNode.innerText = item["levelName"]
                                newNode.setAttribute("class", "machineClass")
                                newNode.onclick = function () {
                                    showDetails(t1 = levelOne, t2 = levelTwo, t3 = item["levelName"])
                                    var nodes = document.getElementById('level3').childNodes
                                    nodes.forEach(function (item, index) {
                                        try {
                                            item.style.backgroundColor = "white"
                                            item.style.color = "grey"
                                        } catch (e) {
                                            //TODO handle the exception
                                        }

                                    })
                                    newNode.style.backgroundColor = "#fb5e33"
                                    newNode.style.color = "white"
                                }
                                level3.appendChild(newNode)
                            })
                        } else {
                            sendMsg(t1 = levelOne, t2 = levelTwo)
                        }

                    }
                })
            }
        })

        document.getElementById('level3').removeAttribute("hidden")


    }

    if (machineType1 && machineType2 && machineType3) {
        levelThree = machineType3
        var level3 = document.getElementById('level3')
        level3.childNodes.forEach(function (item, index) {
            if (item.innerText === levelThree) {
                try {
                    item.style.backgroundColor = "#fb5e33"
                    item.style.color = "white"
                } catch (e) {
                    //TODO handle the exception
                }
            } else {
                try {

                    item.style.backgroundColor = "white"
                    item.style.color = "grey"

                } catch (e) {
                    //TODO handle the exception
                }
            }
        })
        sendMsg(t1 = levelOne, t2 = levelTwo, t3 = machineType3)
    }


}

// 获取翻页
function sendMsg(t1, t2, t3) {
    $.post("/select_list", {
            "levelClassOne": t1,
            "levelClassTwo": t2,
            "levelClassThree": t3,
            "machineSiteId": machineSiteId
        }, function (result) {
            var resultNode = document.getElementById(
                "resultList"
            )
            resultNode.innerHTML = result
        }
    )
}


function rollPage(page) {
    $.post("/rollPage", {
            "page": page
        }, function (result) {
            var resultNode = document.getElementById(
                "resultList"
            )
            resultNode.innerHTML = result
            $(document).scrollTop(200);
        }
    )
}


// 初始化一级目录
function initClassOne() {

    var level1 = document.getElementById("level1")
    machineDict.forEach(function (item, index) {
        let newNode = document.createElement("button")
        newNode.innerText = item.levelName
        newNode.setAttribute("onclick", "showDetails(t1=" + "'" + item.levelName + "'" + ")")
        newNode.onclick = function () {
            showDetails(t1 = item.levelName)
            var nodes = document.getElementById('level1').childNodes
            nodes.forEach(function (item, index) {
                try {
                    item.style.backgroundColor = "white"
                    item.style.color = "grey"
                } catch (e) {
                    //TODO handle the exception
                }

            })
            newNode.style.backgroundColor = "#fb5e33"
            newNode.style.color = "white"

        }
        newNode.setAttribute("class", "machineClass")
        level1.appendChild(newNode)
    })

}
