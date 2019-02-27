D = x => atob(x).split('').map(t => t.charCodeAt(0))

P = D('uNaa16jpzNWIqEf1+Vg3zN7ATPPMlsHojn5UeZj9r97bmriVeJ7sWeW7isXB83x5n4jZ9OzIzfW/5W5JwfN6ptuo7zdHZN5s9/j576PlvjvQiJ+qzPrn/lf0SlTUy+3zx83f2A==')
J = D('ujX4Pzo4tfh5uqb7JHNdnpz0vZIVH2hqaHzvlxEi6hVSlw6SHmOVXo4f2BrvUZXVNlXdylRXFU0YSL2krslW4sxKFhBXJwsd02+T0ZUJ0XepUnJbzpfYVF9UJyLTjglOFUzMyg==')

A = ['#fa9', '#221', '#eac', '#520', '#fff']

F = 0

W = a.width
H = a.height

function R() {
    c.fillStyle = '#ffffff06'
    c.fillRect(0, 0, W, H)
    for(i=0; i<100; i++) {
        idx = J[i]
        pn = P[i]
		xc = (pn % 16) * 40
		yc = Math.floor(pn / 16) * 40
        rr = (Math.floor(idx / 8) % 8) * 20
        colorindex = idx % A.length
        rr += 5 + 5 * Math.sin(F / 7 + i / 7);
        xc += 10 * Math.cos(F / 9 + i / 5 + yc / 9);
		yc += 10 * Math.sin(F / 15 + i / 9);
		xc += W / 2 - 320;
		yc += H / 2 - 320;
        c.fillStyle = A[colorindex] + '1';
        c.beginPath();
		c.arc(xc, yc, rr, 0, Math.PI * 2, true)
        c.fill();
    }
    F ++;
    requestAnimationFrame(R)
}

R()
