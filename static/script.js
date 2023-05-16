window.onload = () => {
    // Themes
    let theme_toggle = document.getElementById("theme-trigger");
    let on = theme_toggle.value;
    theme_toggle.onchange = () => {
        if (theme_toggle.checked) {
            window.localStorage.setItem("theme", "light");
        } else {
            window.localStorage.setItem("theme", "dark");
        }
    }

    // Snowflakes
    if (new Date().getMonth() == 11) {
        let snow_canvas = document.getElementById("snowflakes");
        let snow_ctx = snow_canvas.getContext("2d");
        let snowflakes = [];
        window.onresize = () => {
            snow_ctx.canvas.width = window.innerWidth;
            snow_ctx.canvas.height = window.innerHeight;
            snow_ctx.fillStyle = "#ffffff";
            snow_ctx.globalAlpha = 0.5;

            snowflakes = [];
            for (let i = 0; i < 100; i++) {
                snowflakes.push(
                    {
                        "x": Math.random() * snow_ctx.canvas.width,
                        "y": Math.random() * snow_ctx.canvas.height,
                        "radius": 1 + Math.random(),
                        "vx": 2 + Math.random() * 4,
                        "vy": 10 + Math.random() * 10,
                    }
                );
            }
        };
        window.onresize();
        let last_snow_update = 0;
        const FPS = 20;
        paint_snow = (timestamp) => {
            setTimeout(() => {
                window.requestAnimationFrame(paint_snow);

                let dt = (timestamp - last_snow_update) / 1000 || 0.01;
                last_snow_update = timestamp;

                let num_in_top_left = 0;

                snow_ctx.clearRect(0, 0, snow_ctx.canvas.width, snow_ctx.canvas.height);
                for (let i = 0; i < snowflakes.length; i++) {
                    snowflakes[i].x += snowflakes[i].vx * dt;
                    snowflakes[i].y += snowflakes[i].vy * dt;
                    if (snowflakes[i].y - snowflakes[i].radius > snow_ctx.canvas.height) {
                        snowflakes[i].y = -snowflakes[i].radius;
                    }
                    if (snowflakes[i].x - snowflakes[i].radius > snow_ctx.canvas.width) {
                        snowflakes[i].x = -snowflakes[i].radius;
                    }
                    if (snowflakes[i].x < 50 && snowflakes[i].y < 50) {
                        num_in_top_left++;
                    }

                    snow_ctx.beginPath();
                    snow_ctx.ellipse(snowflakes[i].x,
                        snowflakes[i].y,
                        snowflakes[i].radius,
                        snowflakes[i].radius,
                        0,
                        0,
                        2 * Math.PI);
                    snow_ctx.fill();
                }
                if (num_in_top_left > 20) {
                    setTimeout(window.onresize, 0);
                }
            }, 1000 / FPS);
        };
        paint_snow();
    }

    // Clicking on the page removes the sidebar
    let article = document.querySelector("article");
    article.onclick = () =>  {
        document.querySelector("#nav-trigger-toggle").checked = false;
    };

    // Sliding for side menu
    let body = document.querySelector("body");
    let prev_touches = [];
    let pos_frame_count = 0;
    let neg_frame_count = 0;
    body.ontouchmove = (e) => {
        let touches = [];
        let inc_pos_frame = false;
        let inc_neg_frame = false;
        // TODO(ed): This should probably be in EM, but that requires fancy pants stuff.
        let threshold = 0.25; // pixels / ms
        for (let i = 0; i < e.touches.length; i++) {
            let curr = { x: e.touches[i].pageX, y: e.touches[i].pageY, t: e.timeStamp};
            touches.push(curr);

            if (prev_touches.length > i) {
                let prev = prev_touches[i];
                let delta_t = prev.t - curr.t;
                let delta_x = (prev.x - curr.x) / delta_t;
                let delta_y = (prev.y - curr.y) / delta_t;
                if (Math.abs(delta_x) > 3 * Math.abs(delta_y)) {
                    e.preventDefault();
                    if (delta_x > threshold) {
                        inc_pos_frame = true;
                        pos_frame_count++;
                    } else if (delta_x < -threshold) {
                        inc_neg_frame = true;
                        neg_frame_count++;
                    }
                }
            }
        }
        if (!inc_pos_frame)
            pos_frame_count = 0;
        if (!inc_neg_frame)
            neg_frame_count = 0;
        prev_touches = touches;
        let nav_toggle = document.querySelector("#nav-trigger-toggle");
        if (neg_frame_count > 2) {
            nav_toggle.checked = false;
        }
        if (pos_frame_count > 2) {
            nav_toggle.checked = true;
        }
    }

    // Fancy header image.
    {
        let canvas = document.getElementById("fancy-pants-graphics");
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        let ctx = canvas.getContext("2d");

        let colors = [
            { r: 230, g: 230,   b: 0 },
        ];

        let current_color = Math.floor(Math.random() * colors.length);
        let color_offset = Math.floor(Math.random() * (colors.length - 1) + 1);
        let random_color = () => {
            current_color = (current_color + color_offset) % colors.length;
            return colors[current_color];
        };

        for (let q = 0; q < 2; q++) {
            let x = Math.random() * canvas.width;
            let y = Math.random() * canvas.height;
            let c = random_color();
            ctx.fillStyle = "rgba(" + c.r + ", " + c.g + ", " + c.b + ", 0.2)";
            ctx.beginPath();
            ctx.arc(x, y, canvas.width / 3, 0, 2 * Math.PI);
            ctx.fill();
        }
    }

    // Super secret easter egg
    let secret_password = "LiTHe kod är bäst";
    let secret_password_progress = 0;
    document.querySelector("body").onkeypress = function(e) {
        if (e.key == "s") {
            let nav_toggle = document.querySelector("#nav-trigger-toggle");
            nav_toggle.checked = !nav_toggle.checked;
        }
        if (e.key == "l") {
            let lang = document.querySelector("#toggle-lang");
            lang.click();
        }
        if (e.key == "t") {
            let theme = document.querySelector("#toggle-theme");
            theme.click();
        }
        if (e.key == secret_password[secret_password_progress]) {
            secret_password_progress++;
            if (secret_password_progress == secret_password.length) {
                document.write("<h1>I know ;)</h1>");
            }
        } else {
            secret_password_progress = 0;
        }
        this.dispatchEvent(e);
    };
};
