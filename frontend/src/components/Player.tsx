"use client";

import { Box } from "@mui/material";
import { useRef } from "react";
import useSWRInfinite from "swr/infinite";

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

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const getKey = (pageIndex: number, previousPageData: any[] | null) => {
        if (previousPageData && previousPageData.length === 0) return null;
        return `http://localhost:8000/v1/post/?page=${pageIndex + 1}`;
    };

    const fetcher = () =>
        fetch("http://localhost:8000/v1/post/").then((res) => res.json());

    const { data, error, size, setSize, isLoading, isReachingEnd } =
        useSWRInfinite(getKey, fetcher);

    // console.log("data", data);
    // console.log("error", error);
    // console.log("isLoading", isLoading);

    return (
        <Box
            sx={{
                height: "100vh",
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
                                <div
                                    key={post.uuid}
                                    style={{
                                        height: "100vh",
                                        scrollSnapAlign: "start",
                                        backgroundColor: `#${Math.floor(
                                            Math.random() * 16777215
                                        ).toString(16)}`,
                                    }}
                                >
                                    <h1>{post.title}</h1>
                                    <p>{post.body}</p>
                                </div>
                            ))
                        )}
                    </div>
                )}
            </Box>
            <pre>{JSON.stringify({ data }, null, 2)}</pre>
        </Box>
    );
}
