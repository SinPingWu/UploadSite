####调用Camera进行拍照的过程
Here's a function that invokes an intent to capture a photo.
    ```java
    static final int REQUEST_IMAGE_CAPTURE = 1;

    private void dispatchTakePictureIntent() {
    Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
    if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
        startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        }
    }


####获取缩略图

官网上是这样描述的
>The Android Camera application encodes the photo in the return Intent delivered to onActivityResult() as a small Bitmap in the extras, under the key "data". The following code retrieves this image and displays it in an ImageView.

简而言之就是通过onActivityResult中可以通过getExtras().getdata("data")能获取到返回的缩略图，这个缩略图可以很好的用于Icon的显示，但在其他方面使用不是很好。如果想使用图片文件的话，需要将文件保存在本地。

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            Bundle extras = data.getExtras();
            Bitmap imageBitmap = (Bitmap) extras.get("data");
            mImageView.setImageBitmap(imageBitmap);
        }
    }


>This thumbnail image from "data" might be good for an icon, but not a lot more. Dealing with a full-sized image takes a bit more work.

####保存全屏图片

>The proper directory for shared photos is provided by getExternalStoragePublicDirectory(), with the DIRECTORY_PICTURES argument. Because the directory provided by this method is shared among all apps, reading and writing to it requires the READ_EXTERNAL_STORAGE and WRITE_EXTERNAL_STORAGE permissions, respectively.

>However, if you'd like the photos to remain private to your app only, you can instead use the directory provided by getExternalFilesDir().

我们可以创建私有目录或共有目录来保存图片文件。私有目录只有本APP才能使用，其他应用无法访问，包括Gallery，当应用uninstall后该私有目录也会跟着删除，所以这里我们使用共有目录。

    String mCurrentPhotoPath;

    private File createImageFile() throws IOException {

    // Create an image file name
    String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
    String imageFileName = "JPEG_" + timeStamp + "_";
    // 创建私有目录
    //File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
    // 创建共有目录
    File storageDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);
    File image = File.createTempFile(
        imageFileName,  /* prefix */
        ".jpg",         /* suffix */
        storageDir      /* directory */
    );

    // Save a file: path for use with ACTION_VIEW intents
    mCurrentPhotoPath = "file:" + image.getAbsolutePath();
    return image;
    }

>Note: Files you save in the directories provided by getExternalFilesDir() or getFilesDir() are deleted when the user uninstalls your app.

在此，我们就可以通过以下方法将Camera的文件保存成图片。

    static final int REQUEST_TAKE_PHOTO = 1;

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        // Ensure that there's a camera activity to handle the intent
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            // Create the File where the photo should go
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
                // Error occurred while creating the File
                ...
            }
            // Continue only if the File was successfully created
            if (photoFile != null) {
                Uri photoUri = Uri.fromFile(photoFile);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri);
                startActivityForResult(takePictureIntent, REQUEST_TAKE_PHOTO);
            }
        }
    }


####处理返回的图片文件
在onActivityResult()中可以通过如下的处理来得到图片文件

    BitmapFactory.Options options = new BitmapFactory.Options();
    options.inJustDecodeBounds = true;
    BitmapFactory.decodeFile(mPhotoPath, options);
    int photoW = options.outWidth;
    int photoH = options.outHeight;

    int scaleFactor = (int) Math.min(photoW / BitmapUtils.getScaleX(), photoH / BitmapUtils.getScaleY());

    options.inJustDecodeBounds = false;
    options.inSampleSize = scaleFactor;
    options.inPurgeable = true;

    Bitmap tempBitmap = BitmapFactory.decodeFile(mPhotoPath, options);
    Bitmap bitmap = Bitmap.createScaledBitmap(tempBitmap, (int)BitmapUtils.getScaleX(), (int)BitmapUtils.getScaleY(), true);
    tempBitmap.recycle();

    mImageView.setBackground(new BitmapDrawable(getResources(), bitmap));


####将文件保存到gallery中
到此图片在gallery中还是不可预览的，需要将图片文件插入gallery的数据库中。

    private void galleryAddPicture(final String filePath) {
        ContentValues values = new ContentValues();

        values.put(Images.Media.DATE_TAKEN, System.currentTimeMillis());
        values.put(Images.Media.MIME_TYPE, "image/jpg");
        values.put(MediaStore.MediaColumns.DATA, filePath);

        mContext.getContentResolver().insert(Images.Media.EXTERNAL_CONTENT_URI, values);
    }