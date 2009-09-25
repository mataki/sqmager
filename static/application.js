function onEndCrop( coords, dimensions ) {
  $( 'left' ).value = coords.x1;
  $( 'top' ).value = coords.y1;
  $( 'select_size' ).value = dimensions.width;
}

// with a supplied ratio
Event.observe(
  window,
  'load',
  function() {
    new Cropper.ImgWithPreview(
      'cropper_img',
      {
        ratioDim: { x: 48, y: 48 },
        displayOnInit: true,
        onEndCrop: onEndCrop,
        previewWrap: 'preview'
      }
    );
  }
);
