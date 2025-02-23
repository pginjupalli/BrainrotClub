"use client";

import { Box, Typography } from "@mui/material";
import useSWRInfinite from "swr/infinite";
import React, { useState } from "react";

import Video from "@/components/Video";

export default function Player() {
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

    const [visibleVideo, setVisibleVideo] = useState<string | null>(null);

    const handleVisibilityChange = (uuid: string, visible: boolean) => {
        if (visible) {
            setVisibleVideo(uuid);
        } else if (visibleVideo === uuid) {
            setVisibleVideo(null);
        }
    };

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const getKey = (pageIndex: number, previousPageData: any[] | null) => {
        if (previousPageData && previousPageData.length === 0) return null;
        return `http://localhost:8000/v1/post/?page=${pageIndex + 1}`;
    };

    const fetcher = () =>
        fetch("http://localhost:8000/v1/post/").then((res) => res.json());

    const { data, error, size, setSize, isLoading, isReachingEnd } =
        useSWRInfinite(getKey, fetcher);

    const visiblePost = data
        ?.flat()
        .find((post: Post) => post.uuid === visibleVideo);

    // console.log("data", data);
    // console.log("error", error);
    // console.log("isLoading", isLoading);

    return (
        <Box
            sx={{
                height: "100vh",
                width: "100%",
                display: "flex",
                justifyContent: "center",
            }}
        >
            <Box
                sx={{
                    backgroundColor: "red",
                    height: "100%",
                    aspectRatio: "9 / 16",
                }}
            >
                {error ? (
                    <div>an error occurred</div>
                ) : isLoading ? (
                    <div>loading...</div>
                ) : !data ? (
                    <div>no data</div>
                ) : (
                    <div
                        style={{
                            height: "100%",
                            overflow: "auto",
                            scrollbarWidth: "none",
                            scrollSnapType: "y mandatory",
                            scrollSnapStop: "always",
                        }}
                    >
                        {data.map((page) =>
                            page.map((post: Post) => (
                                <Video
                                    key={post.uuid}
                                    post={post}
                                    onVisibilityChange={handleVisibilityChange}
                                />
                            ))
                        )}
                    </div>
                )}
            </Box>
            <Box
                sx={{
                    backgroundColor: "#e0e0e0",
                    color: "black",
                    height: "100%",
                    width: "500px",
                }}
            >
                <Typography variant="h5">{visiblePost?.club_name}</Typography>
                <Typography variant="h3">{visiblePost?.title}</Typography>
                <Typography variant="p">{visiblePost?.body}</Typography>
            </Box>
        </Box>
    );
}
