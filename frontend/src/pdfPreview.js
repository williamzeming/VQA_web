import React, {PureComponent, useState} from 'react';
import style from './pdfPage.css'

import {Document, Page, pdfjs} from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

export default class PdfPreview extends PureComponent {

    render() {
        const {prfUrl} = this.props


        return (
            <div></div>
            // <div className="pdf-view">
            //     <div className="container">
            //         <Document
            //             file={prfUrl}
            //             onLoadSuccess={this.onDocumentLoadSuccess}
            //             loading={'加载中...'}
            //
            //         >
            //             <Page pageNumber={1} width={500} loading={'loading...'} renderTextLayer={false}/>
            //         </Document>
            //     </div>
            //     <div className="page-tool">
            //         <div className='page-tool-item'> 上一页</div>
            //         <div className='page-tool-item'> 下一页</div>
            //         <div className="input"><input type="number"/> /</div>
            //         <div className='page-tool-item'> 放大</div>
            //         <div className='page-tool-item'> 缩小</div>
            //     </div>
            // </div>
        );
    }
}
