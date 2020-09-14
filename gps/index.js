import 'ol/ol.css';
import {Circle, Fill, Style} from 'ol/style';
import {Feature, Map, Overlay, View} from 'ol/index';
import {OSM, Vector as VectorSource} from 'ol/source';
import {Point} from 'ol/geom';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';
import {useGeographic} from 'ol/proj';

function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;          
}

var imei = '014339000047387';
var json_obj = JSON.parse(Get('http://dweet.io/get/latest/dweet/for/'+imei));
var lat = json_obj['with'][0]['content']['lat'];
var long = json_obj['with'][0]['content']['long'];

useGeographic();

const latestLonLat = [long, lat];

var point = new Point(latestLonLat);

const map = new Map({
  target: 'map',
  view: new View({
    center: latestLonLat,
    zoom: 12
  }),
  layers: [
    new TileLayer({
      source: new OSM()
    }),
    new VectorLayer({
      source: new VectorSource({
        features: [new Feature(point)],
      }),
      style: new Style({
        image: new Circle({
          radius: 9,
          fill: new Fill({color: 'red'}),
        }),
      }),
    })
  ],
});
