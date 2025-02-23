import React from "react";

import { InView } from "react-intersection-observer";

interface Video {
    uuid: string;
    file: string;
    thumbnail: string;
}

interface Post {
    uuid: string;
    club_name: string;
    title: string;
    body: string;
    date_posted: string;
    video: Video;
}

const Video = (post: Post) => {
    <InView
        style={{ height: "100%" }}
        onChange={(inView) => {
            togglePlaying(inView);
            toggleVisible(inView);
        }}
    ></InView>;
};

export default Video;
