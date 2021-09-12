import React, { Component } from 'react';



class PreviousNext extends Component {
    render() {
        return (
            <nav className="navigation post-navigation my-4" role="navigation" aria-label="Posts">
                <div className="nav-links">
                    <div className="nav-previous"><a href="#url" rel="prev">
                        <span className="ast-left-arrow">←</span> Previous Post</a>
                    </div>
                    <div className="nav-next text-right"><a href="#url" rel="next">
                        Next Post <span className="ast-right-arrow">→</span></a>
                    </div>
                </div>
            </nav>
        )
    }
}
export default PreviousNext;