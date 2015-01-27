-   Add full-panel class:

    .full-panel {
        @include position(fixed, $header-height+2.7rem 0px 0px 0px);
        z-index: $zi-panels;
        background-color: transparent;
    }
