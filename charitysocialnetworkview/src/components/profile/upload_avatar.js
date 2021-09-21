import React, { useState, useContext } from "react";
// import "antd/dist/antd.css";
// import "./index.css";
import { Upload, Modal, Button } from "antd";
import IconButton from "@material-ui/core/IconButton";
import PhotoCamera from "@material-ui/icons/PhotoCamera";
import { contexts } from "../../context/context";
import callApi from '../../utils/apiCaller';
import ImgCrop from 'antd-img-crop';

const AvatarImg = () => {
  let context = useContext(contexts)
  const [fileList, setFileList] = useState(
    []
  );
  const [preview, setPreview] = useState({
    previewVisible: false,
    previewImage: "",
  })
  let [loadSucess, setLoadSucess] = useState(false);

  const handleCancel = () => setPreview({ ...preview, previewVisible: false });

  const handlePreview = (file) => {
    setPreview({
      ...preview,
      previewImage: file.thumbUrl,
      previewVisible: true
    });
  };
  const handleUpload = ({ fileList }) => {
    console.log('fileList', fileList);
    setFileList(fileList);
  };


  const handleSubmit = async (event) => {
    event.preventDefault();

    let formData = new FormData();
    // add one or more of your files in FormData
    // again, the original file is located at the `originFileObj` key
    formData.append("avatar", fileList[0].originFileObj);

    let header = { 'content-type': 'multipart/form-data' }
    let url = 'api/accounts/' + `${context.dataProfile.id}` + '/'

    let p = await callApi(url, 'PATCH', formData, header).then(res => {
      if (res.status === 200 || res.status === 201) {
        alert("bạn đã đăng avatar thành công")

      }

    })
    setLoadSucess(true)
  };

  return (
    <div>
      <ImgCrop rotate shape="round" >
        <Upload

          listType="picture-card"
          fileList={fileList}
          onChange={handleUpload}
          onPreview={handlePreview}
          beforeUpload={() => false}
        >
          <IconButton aria-label="upload picture" component="span">
            <PhotoCamera style={{ fontSize: "35px", color: '#aba8a8' }} />
          </IconButton>
          {/* {fileList.length < 2 && "+ Upload"} */}
        </Upload>
      </ImgCrop>

      <Button onClick={handleSubmit} // this button click will trigger the manual upload
      >
        Submit
      </Button>
      <Modal
        visible={preview.previewVisible}
        footer={null}
        onCancel={handleCancel}
      >
        <img alt="example" style={{ width: "100%" }} src={preview.previewImage} />
      </Modal>
    </div>
  );
}
export default AvatarImg;