import React from 'react';

//context list bài post của blog
export const NewsPostContextMod = React.createContext({
    results: [], 
    detail: {},
    comment: [],
    search: false,
})