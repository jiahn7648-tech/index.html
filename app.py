import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정 (제목 등)
st.set_page_config(page_title="내 3D 큐브 앱", layout="wide")

st.title("🧊 Streamlit에서 돌리는 3D 큐브")
st.write("마우스로 아래 큐브를 클릭하고 드래그해보세요!")

# 2. 아까 만든 HTML/JS 코드를 문자열 변수에 담습니다.
# (Three.js 코드를 그대로 가져옵니다)
cube_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #0E1117; } /* 배경을 스트림릿 다크모드와 맞춤 */
        canvas { width: 100%; height: 100%; }
    </style>
</head>
<body>
    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }
        }
    </script>
    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0E1117); // 스트림릿 배경색

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 4;

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        const geometry = new THREE.BoxGeometry(1.5, 1.5, 1.5);
        const material = new THREE.MeshNormalMaterial();
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        function animate() {
            requestAnimationFrame(animate);
            cube.rotation.x += 0.005; // 살짝 자동 회전 추가
            cube.rotation.y += 0.005;
            controls.update();
            renderer.render(scene, camera);
        }
        
        // 창 크기 조절 대응
        window.addEventListener('resize', function() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        animate();
    </script>
</body>
</html>
"""

# 3. 스트림릿 화면에 HTML 렌더링하기
# height를 넉넉하게 주어야 3D 화면이 잘 보입니다.
components.html(cube_html, height=600)
