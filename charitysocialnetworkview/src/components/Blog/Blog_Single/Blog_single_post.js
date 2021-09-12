import React, { Component } from 'react';
import BlogSingleContent from './Blog_single_content';




class BlogSinglePost extends Component {
    render() {
        return (
            <section className="blog-post-main w3l-homeblock1" >
                <div className="blog-content-inf pb-5" style={{textAlign:"none"}}>
                    <BlogSingleContent></BlogSingleContent>
                  
                </div>
            </section>
        )
    }
}
export default BlogSinglePost;