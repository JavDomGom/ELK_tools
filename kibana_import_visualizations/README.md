# Import visualizations to Kibana

1. Se pueden descargar visualizaciones standard manualmente desde la consola de Kibana. Se han de guardar en la carpeta ``templates``.

2. A continuación un ejemplo del contenido del archivo exportado:

  cat templates/export.json | jq ''
```json
[
  {
    "_id": "96af4810-bf62-11e8-8cf3-b72c8cd5aafe",
    "_type": "visualization",
    "_source": {
      "title": "area_01",
      "visState": "{\"title\":\"area_01\",\"type\":\"area\",\"params\":{\"type\":\"area\",\"grid\":{\"categoryLines\":false,\"style\":{\"color\":\"#eee\"}},\"categoryAxes\":[{\"id\":\"CategoryAxis-1\",\"type\":\"category\",\"position\":\"bottom\",\"show\":true,\"style\":{},\"scale\":{\"type\":\"linear\"},\"labels\":{\"show\":true,\"truncate\":100},\"title\":{}}],\"valueAxes\":[{\"id\":\"ValueAxis-1\",\"name\":\"LeftAxis-1\",\"type\":\"value\",\"position\":\"left\",\"show\":true,\"style\":{},\"scale\":{\"type\":\"linear\",\"mode\":\"normal\"},\"labels\":{\"show\":true,\"rotate\":0,\"filter\":false,\"truncate\":100},\"title\":{\"text\":\"Count\"}}],\"seriesParams\":[{\"show\":\"true\",\"type\":\"area\",\"mode\":\"stacked\",\"data\":{\"label\":\"Count\",\"id\":\"1\"},\"drawLinesBetweenPoints\":true,\"showCircles\":true,\"interpolate\":\"linear\",\"valueAxis\":\"ValueAxis-1\"}],\"addTooltip\":true,\"addLegend\":true,\"legendPosition\":\"right\",\"times\":[],\"addTimeMarker\":false},\"aggs\":[{\"id\":\"1\",\"enabled\":true,\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"enabled\":true,\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"h\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{},\"customLabel\":\"Timestamp\"}}]}",
      "uiStateJSON": "{}",
      "description": "",
      "version": 1,
      "kibanaSavedObjectMeta": {
        "searchSourceJSON": "{\"index\":\"38dbf120-bd7d-11e8-8cf3-b72c8cd5aafe\",\"filter\":[],\"query\":{\"query\":\"\",\"language\":\"lucene\"}}"
      }
    }
  }
]
```

3. Inicialmente este formato no es válido para hacer una importación. Para convertirlo a un formato válido se ha de ejecutar el siguiente comando para eliminar algunos campos de la estructura JSON:

  cat templates/export.json | jq '.[]._source'
```json
{
  "title": "area_01",
  "visState": "{\"title\":\"area_01\",\"type\":\"area\",\"params\":{\"type\":\"area\",\"grid\":{\"categoryLines\":false,\"style\":{\"color\":\"#eee\"}},\"categoryAxes\":[{\"id\":\"CategoryAxis-1\",\"type\":\"category\",\"position\":\"bottom\",\"show\":true,\"style\":{},\"scale\":{\"type\":\"linear\"},\"labels\":{\"show\":true,\"truncate\":100},\"title\":{}}],\"valueAxes\":[{\"id\":\"ValueAxis-1\",\"name\":\"LeftAxis-1\",\"type\":\"value\",\"position\":\"left\",\"show\":true,\"style\":{},\"scale\":{\"type\":\"linear\",\"mode\":\"normal\"},\"labels\":{\"show\":true,\"rotate\":0,\"filter\":false,\"truncate\":100},\"title\":{\"text\":\"Count\"}}],\"seriesParams\":[{\"show\":\"true\",\"type\":\"area\",\"mode\":\"stacked\",\"data\":{\"label\":\"Count\",\"id\":\"1\"},\"drawLinesBetweenPoints\":true,\"showCircles\":true,\"interpolate\":\"linear\",\"valueAxis\":\"ValueAxis-1\"}],\"addTooltip\":true,\"addLegend\":true,\"legendPosition\":\"right\",\"times\":[],\"addTimeMarker\":false},\"aggs\":[{\"id\":\"1\",\"enabled\":true,\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"enabled\":true,\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"h\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{},\"customLabel\":\"Timestamp\"}}]}",
  "uiStateJSON": "{}",
  "description": "",
  "version": 1,
  "kibanaSavedObjectMeta": {
    "searchSourceJSON": "{\"index\":\"38dbf120-bd7d-11e8-8cf3-b72c8cd5aafe\",\"filter\":[],\"query\":{\"query\":\"\",\"language\":\"lucene\"}}"
  }
}
```

4. De este modo nos quedamos solo con la estructura que estaba dentro de ``_source`` eliminando todo lo demás.

5. En este punto ya se podría importar, pero antes hay que tener en cuenta que algunas visualizaciones tienen asociado un ID de un index-pattern. Si así fuere hay que modificar el ID del index-pattern por el ID correspondiente del mismo index-pattern con el mismo nombre que se encuentre en el Kibana de destino, es decir, el Kibana donde vamos a importar la visualización. En este ejmplo es la cadena ``38dbf120-bd7d-11e8-8cf3-b72c8cd5aafe``.

6. Una vez realizado el cambio de ID (si fuera necesario) solo hay que ejecutar el script ``addVisualization.sh`` para importar la visualización:

  ```bash
  ./addVisualization.sh
  ```

  En este script hay que setear la variable ``KIBANA``, que tiene como valor la IP y puerto del Kibana de destion, por defecto es: ``http://172.17.0.2:5601``.
