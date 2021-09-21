export function MyCustomUploadAdapterPlugin(editor) {
    editor.plugins.get('FileRepository').createUploadAdapter = (loader) => {
        console.log("load first",loader)
        console.log("ádasdad",Object.keys(editor.plugins),editor.plugins)
        return new MyUploadAdapter(loader)
    }
}

class MyUploadAdapter {
    constructor(props) {
        // CKEditor 5's FileLoader instance.
        this.loader = props;
        // URL where to send files.
        this.url = 'http://localhost:8000/api/newspost/ckeditor/upload/';
    }
 
    // Starts the upload process.
    upload() {
        return new Promise((resolve, reject) => {
            this._initRequest();
            this._initListeners(resolve, reject);
            this._sendRequest();
        });
    }

    // Aborts the upload process.
    abort() {
        if (this.xhr) {
            this.xhr.abort();
        }
    }

    // Example implementation using XMLHttpRequest.
    _initRequest() {
        const xhr = this.xhr = new XMLHttpRequest();

        xhr.open('POST', this.url, true);
        xhr.responseType = 'json';
        xhr.setRequestHeader('Access-Control-Allow-Origin', '*')
        xhr.setRequestHeader('Authorization', localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token'))
    }

    // Initializes XMLHttpRequest listeners.
    _initListeners(resolve, reject) {
        const xhr = this.xhr;
        const loader = this.loader;
        const genericErrorText = `Couldnt upload file: +  ${this.loader.file.name}.`;

        xhr.addEventListener('error', () => reject(genericErrorText));
        xhr.addEventListener('abort', () => reject());
        xhr.addEventListener('load', () => {
            const response = xhr.response;
            if (!response || response.error) {
                return reject(response && response.error ? response.error.message : genericErrorText);
            }

            // If the upload is successful, resolve the upload promise with an object containing
            // at least the "default" URL, pointing to the image on the server.
            console.log("init",this.loader)
            resolve({
                default: response.url
            });
        });

        if (xhr.upload) {
            xhr.upload.addEventListener('progress', evt => {
                if (evt.lengthComputable) {
                    loader.uploadTotal = evt.total;
                    loader.uploaded = evt.loaded;
                }
            });
        }
    }

    // Prepares the data and sends the request.
    _sendRequest() {
       
        console.log("loader",this.loader)
        this.loader.file.then(result => { 
            const data = new FormData();
            console.log("resulet",result)
            data.append('upload', result);
            this.xhr.send(data);
        }
        )
    }
}
