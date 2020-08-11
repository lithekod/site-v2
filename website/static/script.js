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
        // Some doom source code put here for reference.
        let text = `
void G_BuildTiccmd (ticcmd_t* cmd) 
{ 
    int		i; 
    boolean	strafe;
    boolean	bstrafe; 
    int		speed;
    int		tspeed; 
    int		forward;
    int		side;
    
    ticcmd_t*	base;

    base = I_BaseTiccmd ();		// empty, or external driver
    memcpy (cmd,base,sizeof(*cmd)); 
	
    cmd->consistancy = 
	consistancy[consoleplayer][maketic%BACKUPTICS]; 

 
    strafe = gamekeydown[key_strafe] || mousebuttons[mousebstrafe] 
	|| joybuttons[joybstrafe]; 
    speed = gamekeydown[key_speed] || joybuttons[joybspeed];
 
    forward = side = 0;
    
    // use two stage accelerative turning
    // on the keyboard and joystick
    if (joyxmove < 0
	|| joyxmove > 0  
	|| gamekeydown[key_right]
	|| gamekeydown[key_left]) 
	turnheld += ticdup; 
    else 
	turnheld = 0; 

    if (turnheld < SLOWTURNTICS) 
	tspeed = 2;             // slow turn 
    else 
	tspeed = speed;
    
    // let movement keys cancel each other out
    if (strafe) 
    { 
	if (gamekeydown[key_right]) 
	{
	    // fprintf(stderr, "strafe right\n");
	    side += sidemove[speed]; 
	}
	if (gamekeydown[key_left]) 
	{
	    //	fprintf(stderr, "strafe left\n");
	    side -= sidemove[speed]; 
	}
	if (joyxmove > 0) 
	    side += sidemove[speed]; 
	if (joyxmove < 0) 
	    side -= sidemove[speed]; 
 
    } 
    else 
    { 
	if (gamekeydown[key_right]) 
	    cmd->angleturn -= angleturn[tspeed]; 
	if (gamekeydown[key_left]) 
	    cmd->angleturn += angleturn[tspeed]; 
	if (joyxmove > 0) 
	    cmd->angleturn -= angleturn[tspeed]; 
	if (joyxmove < 0) 
	    cmd->angleturn += angleturn[tspeed]; 
    } 
 
    if (gamekeydown[key_up]) 
    {
	// fprintf(stderr, "up\n");
	forward += forwardmove[speed]; 
    }
    if (gamekeydown[key_down]) 
    {
	// fprintf(stderr, "down\n");
	forward -= forwardmove[speed]; 
    }
    if (joyymove < 0) 
	forward += forwardmove[speed]; 
    if (joyymove > 0) 
	forward -= forwardmove[speed]; 
    if (gamekeydown[key_straferight]) 
	side += sidemove[speed]; 
    if (gamekeydown[key_strafeleft]) 
	side -= sidemove[speed];
    
    // buttons
    cmd->chatchar = HU_dequeueChatChar(); 
 
    if (gamekeydown[key_fire] || mousebuttons[mousebfire] 
	|| joybuttons[joybfire]) 
	cmd->buttons |= BT_ATTACK; 
 
    if (gamekeydown[key_use] || joybuttons[joybuse] ) 
    { 
	cmd->buttons |= BT_USE;
	// clear double clicks if hit use button 
	dclicks = 0;                   
    } 

    // chainsaw overrides 
    for (i=0 ; i<NUMWEAPONS-1 ; i++)        
	if (gamekeydown['1'+i]) 
	{ 
	    cmd->buttons |= BT_CHANGE; 
	    cmd->buttons |= i<<BT_WEAPONSHIFT; 
	    break; 
	}`
        let canvas = document.getElementById("fancy-pants-graphics");
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        let ctx = canvas.getContext("2d");

        let colors = [
            { r: 255, g: 255,   b: 0 },
        ];

        let current_color = Math.floor(Math.random() * colors.length);
        let color_offset = Math.floor(Math.random() * (colors.length - 1) + 1);
        let random_color = () => {
            current_color = (current_color + color_offset) % colors.length;
            return colors[current_color];
        };

        const linefeed = 16;
        ctx.font = linefeed + "px monospace";
        ctx.fillStyle = "#DDD";
        ctx.rotate(Math.random * 10 - 0.4);
        let x = -canvas.width * 0.2;
        for (let w = 0; w < 2; w++) {
            x += canvas.width * 0.4;
            let y = -Math.random() * canvas.height;
            let lines = text.split("\n");
            for (let q = 0; q < 20; q++) {
                ctx.fillText(lines[q], x, y);
                y += linefeed;
            }
        }

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
