import React, { useState, useRef } from "react";
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

interface Props {
    post: Post;
}

const Video: React.FC<Props> = ({ post }) => {
    const [visible, setVisible] = useState(false);
    const [playing, setPlaying] = useState(false);

    const vidRef = useRef<HTMLVideoElement>(null);

    const togglePlaying = () => {
        if (playing) {
            setPlaying(false);
            if (vidRef.current) {
                vidRef.current.pause();
            }
        } else {
            setPlaying(true);
            if (vidRef.current) {
                const promise = vidRef.current
                    .play()
                    .catch((err) => console.error(err));
                if (promise !== undefined) {
                    promise.catch(() => {
                        // Autoplay was prevented.
                        vidRef.current!.muted = true;
                        vidRef
                            .current!.play()
                            .catch((err) => console.error(err));
                        vidRef.current!.muted = false;
                    });
                }
            }
        }
    };

    const resetVideo = (visible: boolean) => {
        if (visible) {
            setPlaying(true);
            if (vidRef.current) {
                vidRef.current.play().catch((err) => console.error(err));
                vidRef.current.muted = false;
            }
        } else {
            setPlaying(false);
            if (vidRef.current) {
                vidRef.current.pause();
                vidRef.current.currentTime = 0;
                vidRef.current.muted = true;
            }
        }
    };

    return (
        <InView
            style={{
                height: "100%",
                scrollSnapAlign: "start",
                scrollSnapStop: "always",
            }}
            onChange={(inView) => {
                setVisible(inView);
                resetVideo(inView);
            }}
            threshold={0.75}
        >
            <div style={{ height: "100%", scrollSnapAlign: "start" }}>
                <video
                    ref={vidRef}
                    src={post.video.file}
                    loop={true}
                    style={{ minHeight: "100%", objectFit: "cover" }}
                />
            </div>
        </InView>
    );
};

export default Video;
