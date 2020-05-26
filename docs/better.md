# How do I make the predictions better?

Give the enormous array of forest types and image acquisition environment, it is unlikely that your image will be perfectly predicted by the prebuilt model. Here are some tips to improve predictions

## Check patch size

The prebuilt model was trained on 10cm data at 400px crops. The model is sensitive to predicting to new image resolutions that differ. We have found that increasing the patch size works better on higher quality data. For example, here is a drone collected data () at the standard 400px

```
tile = model.predict_tile("/Users/ben/Desktop/test.jpg",return_plot=True,patch_overlap=0,iou_threshold=0.05,patch_size=400)
```

![](../www/example_patch400.png)

Acceptable, but not ideal.


Here is 1000 px patches.

![](../www/example_patch1000.png)


improved.

## IoU threshold

Object detection models have no inherent logic about overlapping bounding box proposals. For tree crown detection, we expect trees in dense forests to have some overlap, but not be completely intertwined. We therefore apply a postprocessing filter called ‘non-max-suppression’, which is a common approach in the broader computer vision literature. This routine starts with the boxes with the highest confidence scores and removes any overlapping boxes greater than the intersection-over-union threshold (IoU). Intersection-over-union is the most common object detection metric, defined as the area of intersection between two boxes divided by the area of union. If users find that there is too much overlap among boxes, increasing the IoU will return fewer boxes. To in-crease the number of overlapping boxes, reduce the IoU threshold.

## Annotate local training data

Ultimately, training a proper model with local data is the best chance at getting good performance. See DeepForest.train()