import * as THREE from 'three';

// Color map values (Magma)
const colors = [
    "#000004", "#010005", "#010106", "#010108", "#020109", "#02020b", "#02020d",
    "#03030f", "#030312", "#040414", "#050416", "#060518", "#06051a", "#07061c",
    "#08071e", "#090720", "#0a0822", "#0b0924", "#0c0926", "#0d0a29", "#0e0b2b",
    "#100b2d", "#110c2f", "#120d31", "#130d34", "#140e36", "#150e38", "#160f3b",
    "#180f3d", "#19103f", "#1a1042", "#1c1044", "#1d1147", "#1e1149", "#20114b",
    "#21114e", "#221150", "#241253", "#251255", "#271258", "#29115a", "#2a115c",
    "#2c115f", "#2d1161", "#2f1163", "#311165", "#331067", "#341069", "#36106b",
    "#38106c", "#390f6e", "#3b0f70", "#3d0f71", "#3f0f72", "#400f74", "#420f75",
    "#440f76", "#451077", "#471078", "#491078", "#4a1079", "#4c117a", "#4e117b",
    "#4f127b", "#51127c", "#52137c", "#54137d", "#56147d", "#57157e", "#59157e",
    "#5a167e", "#5c167f", "#5d177f", "#5f187f", "#601880", "#621980", "#641a80",
    "#651a80", "#671b80", "#681c81", "#6a1c81", "#6b1d81", "#6d1d81", "#6e1e81",
    "#701f81", "#721f81", "#732081", "#752181", "#762181", "#782281", "#792282",
    "#7b2382", "#7c2382", "#7e2482", "#802582", "#812581", "#832681", "#842681",
    "#862781", "#882781", "#892881", "#8b2981", "#8c2981", "#8e2a81", "#902a81",
    "#912b81", "#932b80", "#942c80", "#962c80", "#982d80", "#992d80", "#9b2e7f",
    "#9c2e7f", "#9e2f7f", "#a02f7f", "#a1307e", "#a3307e", "#a5317e", "#a6317d",
    "#a8327d", "#aa337d", "#ab337c", "#ad347c", "#ae347b", "#b0357b", "#b2357b",
    "#b3367a", "#b5367a", "#b73779", "#b83779", "#ba3878", "#bc3978", "#bd3977",
    "#bf3a77", "#c03a76", "#c23b75", "#c43c75", "#c53c74", "#c73d73", "#c83e73",
    "#ca3e72", "#cc3f71", "#cd4071", "#cf4070", "#d0416f", "#d2426f", "#d3436e",
    "#d5446d", "#d6456c", "#d8456c", "#d9466b", "#db476a", "#dc4869", "#de4968",
    "#df4a68", "#e04c67", "#e24d66", "#e34e65", "#e44f64", "#e55064", "#e75263",
    "#e85362", "#e95462", "#ea5661", "#eb5760", "#ec5860", "#ed5a5f", "#ee5b5e",
    "#ef5d5e", "#f05f5e", "#f1605d", "#f2625d", "#f2645c", "#f3655c", "#f4675c",
    "#f4695c", "#f56b5c", "#f66c5c", "#f66e5c", "#f7705c", "#f7725c", "#f8745c",
    "#f8765c", "#f9785d", "#f9795d", "#f97b5d", "#fa7d5e", "#fa7f5e", "#fa815f",
    "#fb835f", "#fb8560", "#fb8761", "#fc8961", "#fc8a62", "#fc8c63", "#fc8e64",
    "#fc9065", "#fd9266", "#fd9467", "#fd9668", "#fd9869", "#fd9a6a", "#fd9b6b",
    "#fe9d6c", "#fe9f6d", "#fea16e", "#fea36f", "#fea571", "#fea772", "#fea973",
    "#feaa74", "#feac76", "#feae77", "#feb078", "#feb27a", "#feb47b", "#feb67c",
    "#feb77e", "#feb97f", "#febb81", "#febd82", "#febf84", "#fec185", "#fec287",
    "#fec488", "#fec68a", "#fec88c", "#feca8d", "#fecc8f", "#fecd90", "#fecf92",
    "#fed194", "#fed395", "#fed597", "#fed799", "#fed89a", "#fdda9c", "#fddc9e",
    "#fddea0", "#fde0a1", "#fde2a3", "#fde3a5", "#fde5a7", "#fde7a9", "#fde9aa",
    "#fdebac", "#fcecae", "#fceeb0", "#fcf0b2", "#fcf2b4", "#fcf4b6", "#fcf6b8",
    "#fcf7b9", "#fcf9bb", "#fcfbbd", "#fcfdbf"
];

// Convert colors into RGBA data
const width = colors.length;
const height = 1;
const data = new Uint8Array(4 * width * height);
colors.forEach((hex, i) => {
    const color = new THREE.Color(hex);
    const stride = i * 4;
    data[stride] = Math.round(color.r * 255);     // Red
    data[stride + 1] = Math.round(color.g * 255); // Green
    data[stride + 2] = Math.round(color.b * 255); // Blue
    data[stride + 3] = 255;                       // Alpha
});

// Create DataTexture
const colorMapTexture = new THREE.DataTexture(data, width, height, THREE.RGBAFormat);
colorMapTexture.needsUpdate = true;

export default colorMapTexture;