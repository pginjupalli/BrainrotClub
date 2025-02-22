import React from "react";
import { Box, Text } from "@chakra-ui/react";
import { BoxProps } from "@chakra-ui/react";

export default function Logo(props: BoxProps) {
    return (
        <Box {...props}>
            <Text fontSize="lg" fontWeight="bold">
                Logo
            </Text>
        </Box>
    );
}
