window.addEventListener('DOMContentLoaded', event => {
    //    <div class="heatmap" style="height: 500px; width: 400px;"></div>

    // function getUserAvatar() {

    //     document.querySelector('#userAvatar').setAttribute('src', {});
    // }

    async function getUserSessions() {
        await fetch(`${baseUrl}/get_game_sessions`)
            .then(data => data.json())
            .then(data => {
                console.log(data);
                data.userSessionsData.forEach(gameSession => {
                    let heatMapDiv = document.createElement('div');
                    heatMapDiv.style="background-image: url('../static/assets/img/profile/map-image.png');height: 720px;width: 1469px;border: red;border-style: double;margin: 1%;"
                    heatMapDiv.classList.add('heatmap');

                    document.querySelector('#appendHere').append(heatMapDiv);

                    let heatMapData = [];
                    for (let i = 0; i < gameSession.x.length; i++) {
                        let tmp = {
                            x: 0,
                            y: 0,
                            value: 0
                        };
                        tmp.x = +gameSession.x[i];
                        tmp.y = +gameSession.y[i];
                        tmp.value = 1;
                        heatMapData.push(tmp);
                    }

                    console.log(heatMapData);
                    console.log(heatMapDiv);

                    let heatMap = h337.create({
                        container: heatMapDiv
                    });
                    console.log(heatMap);

                    heatMap.setData({
                        max: 1,
                        data: heatMapData
                    });
                });
            })
            .catch(error => console.warn(error));
    }

    getUserSessions();
});