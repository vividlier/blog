KindEditor.ready(function(K) {
                K.create('textarea[id=id_content]',{
                    width:'800px',
                    height:'200px',
                    uploadJson: '/admin/upload/kindeditor',
                });
        });